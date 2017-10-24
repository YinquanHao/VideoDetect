__author__      = "Yinquan Hao"
from flask import render_template
from flask import Flask
from flask import jsonify
from object_detection import objDetect
#from upload import upload
from flask import Response,send_from_directory,send_file,make_response
import vimeo
import time
import datetime
import thread
import os
import re
import vimeo_dl as vimdl

app = Flask(__name__)
app.static_folder = 'static'
app.config['DEBUG'] = False

poolDict = {}

def getfilename(title):
     ok = re.compile(r'[^/]')
     if os.name == "nt":
          ok = re.compile(r'[^\\/:*?"<>|]')
     filename = "".join(x if ok.match(x) else "_" for x in title)
     filename = filename+ ".mp4"
     return filename

@app.route("/")
def init():
    return render_template('index.html')

@app.route("/process/<video_id>")
def ProcessVideo(video_id):
	url="https://vimeo.com/"+video_id
        video = vimdl.new(url)
        if(os.path.isfile("./input/"+video_id+".mp4")):
            print "video already exists"
        else:
            streams = video.streams
            streams[0].download(filepath="./input", quiet=False)
            videoName=video_id+".mp4"
            os.rename("./input/"+getfilename(video.title),"./input/"+videoName)
        return processVideoHandler(video_id)

@app.route("/status/<process_id>")
def GetStatus(process_id):
	print(process_id)
	res = False
	if poolDict[process_id]==True:
		res = True
		poolDict.pop(process_id)
	return jsonify(process_id=process_id,status=res)

def processVideoHandler(video_id):
	ts = time.time()
        print "-----start create processID"
        print ts
        processID = video_id + datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d%H:%M:%S')
        print "------processId:"+processID
	status = False
	thread.start_new_thread(processVideo,(processID,video_id,))
	poolDict[processID] = status
	return jsonify(process_id=processID)

def processVideo(processID,video_id):
	global poolDict
	objDetect.process(video_id)
	#videoLink=upload.uploadVideo("output/"+video_id+"out.mp4")
        #v = vimeo.VimeoClient(
#                token='7d3b39385a75e10b24ff9fdb7afd7525',
#                key='b7ef6a558435d5adcec41f084101ad2cf71a4a50',
#                secret='1v5uooFF5Q4kGzDB++4bWz7ktqjWc+eaIaNP8S3P/UPHktfoQhYi5zpWq1lS9Y7fOR32jSavbtFSOXoDijYAuR4qn/Se+prE64hnXS8nVbkwArZRXa1fJccO1dd7iXfZ')
#        video_uri = v.upload("output/"+video_id+"out.mp4")
#        print video_uri
#        v.patch(video_uri, data={'name': 'uploadtest', 'description': '...'})
#	videoLink="https://vimeo.com/"+video_uri[8:]
#        print videoLink
	poolDict[processID] = True

@app.route("/download/<video_id>",methods=['GET','POST'])
def download(video_id):
	#print video_id
	#csv = '1,2,3\n4,5,6\n'
        #return Response(csv,mimetype="text/csv",headers={"Content-disposition":"attachment; filename=myplot.csv"})
        root_dir=os.path.dirname(os.getcwd())
        #print root_dir
        #video=open(root_dir+"/objectRecModels/output/"+video_id+"out.mp4")
        #return send_from_directory(root_dir+"/objectRecModels/output",video_id+"out.mp4",as_attachment=True)
        #return Response(video,mimetype="video/mp4",headers={"Content-disposition":"attachment; filename=result.mp4"}) 
        #size=os.path.getsize(root_dir+"/objectRecModels/output/"+video_id)
        name='result.mp4'
        response=make_response()
        #response.headers['Content-Description'] = 'File Transfer'
        response.headers['Cache-Control'] = 'no-cache'
        response.headers['Content-Type']="application/octet-stream"
        response.headers['Content-Disposition'] = 'attachment; filename=%s' % name
        #response.headers['Content-Disposition']='attachment'
        #response.headers['Content-Length'] = size
        response.headers['X-Accel-Redirect'] ='/download/'+video_id
        return response

if __name__ == "__main__":
	app.run()
