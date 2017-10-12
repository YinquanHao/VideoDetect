# VideoDetect
The VideoDetect infrastructures

# Install Tensorflow on Ubuntu
$ sudo apt-get install python-pip python-dev \n
$ pip install --no-cache-dir tensorflow

# Install Opencv
$ pip install opencv-python

# Install python Image
$ pip install image

# Install The gRPC protocal Buffer
Download the protobuf-cpp-3.4.1.zip from https://github.com/google/protobuf/releases. \n
$ ./configure \n
$ make
$ make check
$ sudo make install
$ sudo ldconfig # refresh shared library cache.

# Compile the proto2 in the object_detection
$ protoc object_detection/protos/*.proto --python_out=.

#



