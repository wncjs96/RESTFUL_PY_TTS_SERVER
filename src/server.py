from flask import Flask, request, jsonify, send_from_directory
import pyttsx3
import os

app = Flask(__name__)

UPLOAD_DIRECTORY = "uploaded_files"
if not os.path.exists(UPLOAD_DIRECTORY):
	os.makedirs(UPLOAD_DIRECTORY)

#speaker_id: 0 for male 1 for female
#volume : min = 0 max = 1
#speed : min = 0 max = 3
def_setting = {"text": "","speaker_id": 0,"volume": 1,"speed": 1}

# POST
@app.route('/conversion', methods = ['POST'])
def conversion():
	data = request.get_json()
	tts(data)
	return send_from_directory(UPLOAD_DIRECTORY, "temp.mp3", as_attachment=True)

# GET
# For testing
@app.route('/setting')
def setting():
	return jsonify(def_setting)

@app.route('/files')
def list_files():
	files = []
	for filename in os.listdir(UPLOAD_DIRECTORY):
		path = os.path.join(UPLOAD_DIRECTORY, filename)
		if os.path.isfile(path):
			files.append(filename)
	return jsonify(files)

@app.route('/files/<path:path>')
def get_file(path):
	return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)

# TTS
def tts(data):
	engine = pyttsx3.init()
	# Setting
	engine.setProperty('rate', data["speed"]*100)
	engine.setProperty('volume', data["volume"])
	voices = engine.getProperty('voices')
	engine.setProperty('voice', voices[data["speaker_id"]].id)
	engine.save_to_file(data["text"], 'uploaded_files/temp.mp3')
	engine.runAndWait()
	return

if __name__ == "__main__":
	app.run()
	
