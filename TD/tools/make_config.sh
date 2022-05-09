#!/us/bin/env bash
../external/darknet/darknet detector calc_anchors configs/TD.data -num_of_clusters 3 -width 224 -height 224 -show 0
value=$(<anchors.txt)
echo "$value"
sed -i '/anchors/ s/\=.*/= '"$value"' /g' configs/TD.cfg