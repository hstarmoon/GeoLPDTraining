# Geo LPD training

This repository contains LPD and TD training code.

## Installation

### Option 1: Step-by-step installation
```bash
  # first, make sure that your conda is setup properly with the right environment
  # for that, check that `which conda`, `which pip` and `which python` points to the
  # right path. From a clean conda env, this is what you need to do

  conda create --name geoLPD -y python=3.6
  conda activate geoLPD

  # this installs the right pip and dependencies for the fresh python
  conda install ipython pip

  # clone repo
  git clone https://github.com/olala313/GeoLPDTraining.git
  cd GeoLPDTraining/
  
  # Create environment and build:
  bash init_venv.sh


```

### Data prepare

To clean data ,run the command:

```bash

python3 tools/geo_data_clean_me.py --data_dir /root/data/ --output_dir /root/workspace/GeoLPDTraining-master/test_o/
python3 tools/geo_data_clean_me.py --data_dir /root/EVS_data/ --output_dir /root/workspace/GeoLPDTraining-master/test_o/																																		

python tools/geo_data_clean.py --data_dir D:\data\Myanmar\Myanmar_backup/ --output_dir D:\data\Myanmar\test_clean/
```
and convert LPD data, run the command:
```bash
python3 LPD/tools/geo2LPD_new.py --data_dir "train_copy/" --output_dir "train_copy2/" --offset 20
python3 LPD/tools/geo2LPD.py --data_dir "train_clean/" --output_dir "train_LPD_20/" --offset 20
python3 TD/tools/geo2TD.py --data_dir "train_clean/" --output_dir "test_TD_20/" --offset 20
python3 TD/tools/geo2TD_muti_new.py --data_dir "test_clean/" --output_dir "test_TD_102030/" --offset 20
```
get pre-train model
```
bash tools/download_pretrain.sh
```

### Training
```cd LPD``` or ```cd TD```

Content of the file `/configs/LPD.data` should be
```
python random_train.py --data_dir /workspace/data/GeoLPDTraining-master/train_LPD_20/ --mode i --train_rate 1
train  = <replace with your path>/train.txt
valid = <replace with your path>/test.txt
```
Make anchors to cfg:
```
bash tools/make_config.sh
```
training
```
bash tools/train.sh
```

測試MAP
../external/darknet/darknet detector map ./configs/LPD.data ./configs/LPD.cfg ./model/LPD_final.weights
../external/darknet/darknet detector map ./configs/TD.data ./configs/TD.cfg ./model/TD_final.weights
