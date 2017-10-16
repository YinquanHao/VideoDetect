__author__      = "Yinquan Hao"
from flask import Flask
from flask import jsonify
from objDetect import process
import time
import datetime
import thread
app = Flask(__name__)
app.config['DEBUG'] = False

poolDict = {}
ts = time.time()

@app.route("/")
def hello():
    return "HelWorld!"

@app.route("/process/<video_id>")
def ProcessVideo(video_id):
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
	processID = video_id + datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d%H:%M:%S')
	status = False
	thread.start_new_thread(processVideo,(processID,video_id,))
	poolDict[processID] = status
	return jsonify(process_id=processID)

def processVideo(processID,video_id):
	global poolDict
	process(video_id)
	poolDict[processID] = True