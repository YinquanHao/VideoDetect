# VideoDetect
The VideoDetect infrastructures

# Install Tensorflow on Ubuntu
$ sudo apt-get install python-pip python-dev <br />
$ pip install --no-cache-dir tensorflow <br />

# Install Opencv
$ pip install opencv-python <br />

# Install python Image
$ pip install image <br />

# Install The gRPC protocal Buffer
Download the protobuf-cpp-3.4.1.zip from https://github.com/google/protobuf/releases. <br />
$ ./configure <br />
$ make <br />
$ make check <br />
$ sudo make install <br />
$ sudo ldconfig # refresh shared library cache. <br />

# Compile the proto2 in the object_detection
$ protoc object_detection/protos/*.proto --python_out=. <br />

#



