../external/darknet/darknet detector train configs/LPD.data configs/LPD.cfg ../tools/yolov3-tiny.conv.15 -clear -dont_show -gpus 2 2>&1 | tee model/train.log