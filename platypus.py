import os
import json
from os.path import join, dirname
from dotenv import load_dotenv
from watson_developer_cloud import SpeechToTextV1 as SpeechToText
from watson_developer_cloud import TextToSpeechV1
from watson_developer_cloud import NaturalLanguageClassifierV1

def main():
	#initiate conversation here
	print("Please say something nice into the microphone\n")

if __name__ == '__main__':
	dotenv_path = os.path.join(os.path.dirname(__file__),'platypus.env')
	load_dotenv(dotenv_path)
	try:
		main()
	except:
		print("IOError detected, restarting...")
		main()

