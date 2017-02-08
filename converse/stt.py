import os
from os.path import join, dirname
from dotenv import load_dotenv
from ws4py.client.threadedclient import WebSocketClient
import base64, time, json, ssl, subprocess, threading

def getEnv():
	dotenv_path = os.path.join(os.path.dirname(__file__),'platypus.env')
	load_dotenv(dotenv_path)
	username = os.environ.get("SPEECH_TO_TEXT_USERNAME")
	password = os.environ.get("SPEECH_TO_TEXT_PASSWORD")
	auth_string = "%s:%s" % (username, password)
	return auth_string	

class SpeechToTextClient(WebSocketClient):
    def __init__(self):
        ws_url = "wss://stream.watsonplatform.net/speech-to-text/api/v1/recognize"
        environment = getEnv()
        base64string = base64.encodestring(environment).replace("\n", "")
        self.listening = False
        try:
            WebSocketClient.__init__(self, ws_url,
                headers=[("Authorization", "Basic %s" % base64string)])
            self.connect()
        except: print "Failed to open WebSocket."

    def opened(self):
        self.send('{"action": "start", "content-type": "audio/l16;rate=16000", "inactivity_timeout": 5}')
        self.stream_audio_thread = threading.Thread(target=self.stream_audio)
        self.stream_audio_thread.start()

    def received_message(self, message):
        message = json.loads(str(message))
        if "state" in message:
            if message["state"] == "listening":
                self.listening = True
        print "Message received: " + str(message)

        if "results" in message:
        	content = ""

        	if (len(message["results"])==0):
        		print("Watson returned an empty STT guess")
        	else:
        		content = message["results"][0]["alternatives"][0]["transcript"]
        		print content
        		#SpeechToTextClient.close(self)
        		self.listening = False


    def stream_audio(self):
        while not self.listening:
        	time.sleep(0.1)

        reccmd = ["arecord", "-f", "S16_LE", "-r", "16000", "-t", "raw"]
        p = subprocess.Popen(reccmd, stdout=subprocess.PIPE)

        while self.listening:
            data = p.stdout.read(1024)

            try: 
            	self.send(bytearray(data), binary=True)
            	#print ("testing testing")
            except ssl.SSLError: 
            	print("SSLError")
            	pass

        print("done looping")
        p.kill()
        print "killed it"

    def close(self):
        self.listening = False
        print("Getting ready to exit thread...")
        self.stream_audio_thread.join()
        print("Exited thread successfuly")
        WebSocketClient.close(self)


try:
    stt_client = SpeechToTextClient()
    raw_input()
finally:
    stt_client.close()
