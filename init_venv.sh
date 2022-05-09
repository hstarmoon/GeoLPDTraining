#!/us/bin/env bash
cat requirements.txt | xargs -n 1 -L 1 pip3 install

git submodule update --init --recursive external/darknet/

cd external/darknet/ 

git checkout 4d9adde 

mkdir build-release
cd build-release
cmake ..
make -j 40
make install -j 40