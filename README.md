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

# Serving the Infra on EC2 using gunicorn <br />
$ pip install gunicorn <br />
$ sudo yum install nginx <br />
$ sudo vi /etc/nginx/nginx.conf <br />
 replace the file with <br />
 '''
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
 '''

$ sudo /etc/rc.d/init.d/nginx start <br />
$ gunicorn videoserver:app -b localhost:8000 & <br />


