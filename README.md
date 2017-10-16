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

# Run the object rec
$ python objectRecModels/objDetect.py <br />
output image will be save in /output_imgs <br />

# Install python moviepy
$ pip install moviepy  <br />
$ pip install imageio  <br />

# login to aws webservice
$ chmod 400 /yinhao.pem  <br />
$ ssh -i yinhao.pem ec2-user@ec2-18-221-61-248.us-east-2.compute.amazonaws.com  <br />

# Install the gRPC to the aws ec2
$ scp -i yinhao.pem ../protobuf-cpp-3.4.1.zip ec2-user@ec2-18-221-61-248.us-east-2.compute.amazonaws.com:~/  <br />
$ sudo yum groupinstall "Development tools"  <br />

