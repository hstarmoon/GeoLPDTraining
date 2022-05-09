# -*- encoding:utf-8 -*-
import os
import sys
import glob
import argparse
import cv2
import random
import shutil


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


def label_rule_checker(labels):
    try:
        for label in labels:
            if len(label) != 8:
                print(' label len is not 8')
                return False
    except:
        return False
    else:
        return labels


def convert(img, box, expand=0):
    dw = 1. / (img.shape[1])
    dh = 1. / (img.shape[0])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    y = y * dh
    if (expand):
        w = w * expand
        h = h * (expand + 0.2)
    w = w * dw
    h = h * dh
    return (x, y, w, h)


def label_transfer(img, labels, offset=0):
    img_w = img.shape[1]
    img_h = img.shape[0]
    rects = []
    for label in labels:
        tl = [None] * 2
        br = [None] * 2

        tl[0] = min(label[0], label[2])
        tl[1] = min(label[1], label[7])

        br[0] = max(label[4], label[6])
        br[1] = max(label[3], label[5])

        if (offset):
            expand = random.randint(20, offset)
            print(expand)
            expand = (expand / 100) + 1

        x, y, width, height = convert(img, (tl[0], br[0], tl[1], br[1]), expand)
        rect = [0, x, y, width, height]
        if 0:
            img_plot = img
            cv2.rectangle(img_plot, (int(x * img_w - width * img_w / 2), int(y * img_h - height * img_h / 2)),
                          (int(x * img_w + width * img_w / 2), int(y * img_h + height * img_h / 2)), (50, 255, 50), 2)
            cv2.imshow('img_plot', img_plot)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        rects.append(rect)
    return rects


def main():
    parser = argparse.ArgumentParser(prog='geo2LPD')
    parser.add_argument('--data_dir', type=str, default="", required=False,
                        help='Path to input data\n')
    parser.add_argument('--output_dir', type=str, default='', required=False,
                        help='Output directory\n')
    parser.add_argument('--offset', default=30, type=int,
                        help='Extend box width and height,unit is percentage\n')

    args = parser.parse_args()
    total = 0
    savepath = args.output_dir
    createFolder(savepath)
    try:
        for root, dirs, files in os.walk(args.data_dir):
            for cur_dir in dirs:
                createFolder(os.path.join(savepath, os.path.relpath(root, args.data_dir), cur_dir))
                print("createFolder")
            for txtfiles in glob.glob(os.path.join(root, "*.txt")):
                print(txtfiles)
                imagepath = txtfiles[:-3] + ('jpg')
                img = cv2.imread(imagepath)
                if img is None:
                    print('NoneType')
                    continue
                with open(txtfiles, 'r',encoding='utf-8') as txtfile:
                    all_lines = txtfile.readlines()
                # print(all_lines)
                labels = [line.rsplit(' ')[0].split(',') for line in all_lines]
                # labels=label_rule_checker(labels)
                if (labels):
                    labels = [[float(i) for i in label] for label in labels]
                    rects = label_transfer(img, labels, args.offset)
                    rects = [[str(i) for i in rect] for rect in rects]
                    modifyLabels = list(map(' '.join, rects))
                    with open(os.path.join(savepath, os.path.relpath(txtfiles, args.data_dir)), 'w+',encoding='utf-8') as outfile:
                        [outfile.write(modifyLabel + '\n') for modifyLabel in modifyLabels]
                        shutil.copyfile(imagepath,
                                        os.path.join(savepath, os.path.relpath(txtfiles, args.data_dir))[:-3] + ('jpg'))
                        total += 1
        print('Total data : ' + str(total))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print('------------start------------')
    sys.exit(main() or 0)
    print('------------end------------')

