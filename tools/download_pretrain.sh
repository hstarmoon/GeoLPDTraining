wget -c -O tools/yolov3-tiny.weights https://pjreddie.com/media/files/yolov3-tiny.weights

external/darknet/darknet partial external/darknet/cfg/yolov3-tiny.cfg tools/yolov3-tiny.weights tools/yolov3-tiny.conv.15 15