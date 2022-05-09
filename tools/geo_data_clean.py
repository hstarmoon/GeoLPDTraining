import os
import sys
import glob
import argparse
import cv2
import shutil

def argparser():
    parser = argparse.ArgumentParser(prog='data clean')
    parser.add_argument('--data_dir',   type = str, default = r'D:\data\Myanmar\test50', required=False,
                        help='Path to input directory\n' )
    parser.add_argument('--output_dir', type = str, default = r'D:\data\Myanmar\test50_clean', required=False,
                        help='Output directory\n' ) 
    return parser

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
        
def label_rule_checker(labels,img_shape):
    labels = data_clean(labels,img_shape)
#    labels = two_column_check(labels)
    try:
        for label in labels:
            if int(label[2]) == 0:
                return False
            anno=list(map(int, label[0].split(',')))
            if (anno[4]+anno[5]-anno[0]-anno[1]) <= 0:
                return False
    except :
        return False
    else:
        return labels

def two_column_check(labels):
    return [label for label in labels if label[1].index('@')==0]   
def data_clean(labels,img_shape):
    return [anno_Modify(label,img_shape) for label in labels if len(label) == 3]

def anno_Modify(label,img_shape):
    anno=list(map(int, label[0].split(',')))
    anno=[max(min(img_shape[(x+1) % 2], anno[x]), 0) for x in range(len(anno))]
    label[0]=','.join(str(x) for x in anno)
    return label

def main():
    args = argparser().parse_args()
    total=0
    noise=0
    badimg=0
    savepath = args.output_dir
    createFolder(savepath)
    try:
        for root, dirs, files in os.walk(args.data_dir):
            for cur_dir in dirs:
                createFolder(os.path.join(savepath,os.path.relpath(root, args.data_dir),cur_dir))
            for txtfiles in glob.glob(os.path.join(root,"*.txt")):
                total+=1
                imagepath=txtfiles[:-3]+('jpg')
                img=cv2.imread(imagepath)
                if img is None:
                    print(os.path.basename(imagepath) +' NoneType')
                    badimg+=1
                    continue                
                with open(txtfiles,'r') as txtfile:
                    all_lines = txtfile.readlines()
                labels=[line.strip().split(' ') for line in all_lines]
                labels=label_rule_checker(labels,img.shape)
                if(labels):
                    modifyLabels=list(map(' '.join, labels))
                    with open(os.path.join(savepath,os.path.relpath(txtfiles, args.data_dir)),'w+') as outfile:
                        [outfile.write(modifyLabel+'\n') for modifyLabel in modifyLabels]
                    shutil.copyfile(imagepath,os.path.join(savepath,os.path.relpath(txtfiles, args.data_dir))[:-3]+('jpg'))
                else:
                    noise+=1
                    print(os.path.basename(txtfiles)+' is noise data')
        print('Total data : '+str(total))
        print('Noise data : '+str(noise))
        print('badimg data : '+str(badimg))
    except Exception as e :
        print(e)
if __name__ == '__main__':
    sys.exit(main() or 0)
                
                