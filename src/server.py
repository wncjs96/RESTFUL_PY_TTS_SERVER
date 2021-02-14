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

engine = pyttsx3.init()
voices = engine.getProperty('voices')

# POST
@app.route('/api/conversion', methods = ['POST'])
def conversion():
	data = request.get_json()
	tts(data)
	return send_from_directory(UPLOAD_DIRECTORY, "temp.mp3", as_attachment=True)

# GET
# For testing
@app.route('/api/setting')
def setting():
	return jsonify(def_setting)

# TODO: Server should not be able to access the client's upload directory
@app.route('/api/files')
def list_files():
	files = []
	for filename in os.listdir(UPLOAD_DIRECTORY):
		path = os.path.join(UPLOAD_DIRECTORY, filename)
		if os.path.isfile(path):
			files.append(filename)
	return jsonify(files)

#TODO: list voices first, find out which languages/voices are being supported, new way to add languages, voices, then send them back
@app.route('/api/voices')
def list_voices():
	result = []
	for voice in voices:
		#print("Voice:")
		#print(" - ID: %s" % voice.id)
		#print(" - Name: %s" % voice.name)
		#print(" - Languages: %s" % voice.languages)
		#print(" - Gender: %s" % voice.gender)
		#print(" - Age: %s" % voice.age)
		#print(str(voice.id))
		result.append(str(voice.id))
	return jsonify(result)


@app.route('/api/files/<path:path>')
def get_file(path):
	return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)



# TTS
def tts(data):
	#engine = pyttsx3.init()
	# Setting
	engine.setProperty('rate', data["speed"]*100)
	engine.setProperty('volume', data["volume"])
	#voices = engine.getProperty('voices')
	#list_voices(voices)
	#print(voices[0].id)
	engine.setProperty('voice', voices[int(data["speaker_id"])].id)
	#TODO: remove Korean Setup
	#engine.setProperty('voice', voices[0].id)
	engine.save_to_file(data["text"], 'uploaded_files/temp.mp3')
	engine.runAndWait()
	return


if __name__ == "__main__":
	app.run()
	
