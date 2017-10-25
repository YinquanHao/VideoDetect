# VideoDetect
## The VideoDetect infrastructure
Yinquan Hao <br />
Lie Han <br />

The VideoDetect infrastructures would detect the object in the video and render boxes and labels on the output video.<br />

![alt text](https://github.com/YinquanHao/VideoDetect/blob/master/objectRecModels/output_imgs/sample.png)

## Technologies Used In the VideoDetect

### Backend
Tensorflow<br />
Opencv<br />
python Image<br />
Numpy<br />
PILLOW<br />
gRpc<br />

### Frontend & Web App
Flask<br />
Nginx<br />
Jquery<br />
gunicorn<br />

### Cloud and Video Host
Amazon Ec2<br />
Vimeo Video Host<br />

## Brief pipeline of the infrastructure

1) The Web Application would take a videoID of Vimeo from the user.<br />

2) The videoID would be sent to the backend service as a request.<br />

3) The backend service adds a new thread to the thread pool to process the video and mark the newly added thread's status as in process.<br />

3a) The backend service would download the video from the Vimeo.<br />

3b) The backend service would break down the video frame by frame.<br />

3c) For each frame it would use the Object Detection Model to detect the objects in the frame.<br />

3d) The backend service re-combine the frames to an output video and save it.<br />

3e) The backend service make the thread status as done.<br />

4) The backend service would generate a unique process_id and send it back to client side.<br />

5) The client would send a request to server side to check if the worker thread corresponding to process_id is done.<br />

5a) If the backend's response shows the status as in process repeat step 5.<br />

5b) client side would open a video stream if the backend's response shows the status as done.<br />


# Using and testing
goto: http://ec2-13-58-97-89.us-east-2.compute.amazonaws.com/<br />

Input the videoID on viemo, current we only support MP4 format. Example 238003958<br />

The process takes as long as 5 to 10 mins, due to the limit resource from EC2 :<<br />

After the process finished, a video would play.<br />



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

# Serving the Infra on EC2 using gunicorn <br />
$ pip install gunicorn <br />
$ sudo yum install nginx <br />
$ sudo vi /etc/nginx/nginx.conf <br />
 replace the file with <br />

```
user ec2-user;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /var/run/nginx.pid;

include /usr/share/nginx/modules/*.conf;

events {
    worker_connections 1024;
}

http {
    server_names_hash_bucket_size 128;
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 2048;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    include /etc/nginx/conf.d/*.conf;

    index   index.html index.htm;

    server {
         listen       80;
   	 server_name  your_public_dnsname_here;

   	 location / {
        	proxy_pass http://127.0.0.1:8000;
    	 }	
}
```

$ sudo /etc/rc.d/init.d/nginx start <br />
$ gunicorn videoserver:app -b localhost:8000 & <br />


