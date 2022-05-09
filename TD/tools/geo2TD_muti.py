#coding: UTF-8
import os
import sys
import glob
import argparse
import cv2
import random

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
def label_rule_checker(labels,img_shape):
    try:
        for label in labels:
            if int(label[2]) != 1:
                labels.remove(label)
                continue
            anno=list(map(int, label[0].split(',')))
            if (anno[4]+anno[5]-anno[0]-anno[1]) <= 0:
                labels.remove(label)
                continue
    except :
        return False
    else:
        return labels
def label_transfer(img,label,offset_start, offset):
    tl=[None]*2
    br=[None]*2
    
    tl[0]=min(label[0],label[2])
    tl[1]=min(label[1],label[7])
    
    br[0]=max(label[4],label[6])
    br[1]=max(label[3],label[5])
    
    offset= random.randint(offset_start, offset)
    offset=(offset/100)+1
    width = round((br[0]-tl[0])*offset)
    height =round((br[1]-tl[1])*(offset+0.3))
    if(offset>1.5):
        mid_x = round(((tl[0]+br[0])*random.uniform(0.45,0.55)))
        mid_y = round(((tl[1]+br[1])*random.uniform(0.45,0.55)))
    else:
        mid_x = round(((tl[0]+br[0])*0.5))
        mid_y = round(((tl[1]+br[1])*0.5))
    tl[0]=round(max(mid_x-(width/2),0))
    tl[1]=round(max(mid_y-(height/2),0))
    br[0]=round(min(mid_x+(width/2),img.shape[1]))
    br[1]=round(min(mid_y+(height/2),img.shape[0]))
    
    img_crop=img[int(tl[1]):int(br[1]),int(tl[0]):int(br[0])]
    
    label_crop =[float(i) for i in label]
    for i in range(0,7,2):
        label_crop[i]-=tl[0]
        label_crop[i+1]-=tl[1]
    return img_crop,label_crop
def save_jpgandtxt(crop_img,label_crop,savepath,outfilename):
    path=os.path.join(savepath,outfilename)
    img_w=crop_img.shape[1]
    img_h=crop_img.shape[0]
    with open(path,'w+') as outfile:
        for i in range(0,7,2):
            mid_x = round(label_crop[i]/img_w,6)
            mid_y = round(label_crop[i+1]/img_h,6)
            if mid_x > 0 and mid_x < 1 and mid_y > 0 and mid_y < 1:
                label_width = 0.100000
                label_height = 0.200000
                print(' '.join( [str(i) for i in [int(i/2),mid_x,mid_y,label_width,label_height]]))
                outfile.write(' '.join( [str(i) for i in [int(i/2),mid_x,mid_y,label_width,label_height]])+'\n')
        cv2.imwrite(path[:-3]+('jpg'), crop_img)


def main(argv):
    parser = argparse.ArgumentParser(prog='geo2TD')
    parser.add_argument('--data_dir',   type = str, default = r'D:\RD\Project\GeoLPDTraining-master\TD\tools\123', required=False,
                        help='Path to input data\n' )
    parser.add_argument('--output_dir', type = str, default = r'D:\RD\Project\GeoLPDTraining-master\TD\tools\456', required=False,
                        help='Output directory\n' )   
    parser.add_argument('--offset', default = 30, type = int,
                        help='Extend box width and height,unit is percentage\n' ) 

    args = parser.parse_args()
    savepath = args.output_dir

    offset_1 = 20
    total=0
    
    try:
        for root, dirs, files in os.walk(args.data_dir):
            for cur_dir in dirs:
                createFolder(os.path.join(savepath,os.path.relpath(root, args.data_dir),cur_dir))
            for txtfiles in glob.glob(os.path.join(root,"*.txt")):
                img_path=txtfiles[:-3]+('jpg')
                img=cv2.imread(img_path)
                print(img_path)
                if img is None:
                    print(os.path.basename(img_path) +' is NoneType')
                    continue     
                with open(txtfiles,'r', errors='replace') as txtfile:
                    all_lines = txtfile.readlines()
                labels=[line.strip().split(' ') for line in all_lines]
                labels=label_rule_checker(labels,img.shape)
                if(labels):
                    float_labels=[[float(i) for i in label[0].split(',')]for label in labels]
                    for i,float_label in enumerate(float_labels):
                        crop_img,label_crop=label_transfer(img,float_label, 10, offset_1)
                        save_jpgandtxt(crop_img, label_crop, os.path.join(savepath, os.path.relpath(os.path.dirname(txtfiles), args.data_dir)), '_'+str(i)+'_'+os.path.basename(txtfiles))

                        crop_img, label_crop = label_transfer(img, float_label, offset_1, args.offset)
                        save_jpgandtxt(crop_img, label_crop, os.path.join(savepath, os.path.relpath(os.path.dirname(txtfiles), args.data_dir)), '_' + str(i) + '_20_' + os.path.basename(txtfiles))

                        # crop_img, label_crop = label_transfer(img, float_label, args.offset)
                        # save_jpgandtxt(crop_img, label_crop, os.path.join(savepath, os.path.relpath(os.path.dirname(txtfiles), args.data_dir)), '_' + str(i) + '_' + os.path.basename(txtfiles))

                        total+=1
        print('Total data : '+str(total))
    except Exception as e :
        print(e)
if __name__ == '__main__':
    print('------------start------------')
    main(sys.argv)
    print('------------end------------')
                
                