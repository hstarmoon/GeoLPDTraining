#!/us/bin/env bash
../external/darknet/darknet detector calc_anchors configs/LPD.data -num_of_clusters 6 -width 416 -height 416 -show 0
value=$(<anchors.txt)
echo "$value"
sed -i '/anchors/ s/\=.*/= '"$value"' /g' configs/LPD.cfg