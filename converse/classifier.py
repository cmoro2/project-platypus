import os
from os.path import join, dirname
from dotenv import load_dotenv
from watson_developer_cloud import NaturalLanguageClassifierV1
import json

def getUser():
	dotenv_path = os.path.join(os.path.dirname(__file__),'platypus.env')
	load_dotenv(dotenv_path)
	username = os.environ.get("NLC_USERNAME")
	return username

def getPassword():
	dotenv_path = os.path.join(os.path.dirname(__file__),'platypus.env')
	load_dotenv(dotenv_path)
	password = os.environ.get("NLC_PASSWORD")
	return password
	

natural_language_classifier = NaturalLanguageClassifierV1(
	#username = '8d370748-bbf4-4f01-95b4-42d877e94ed7',
	#password = 'jSKoVNJWlGHV'
	username = getUser(),
	password = getPassword()
	)

#def train_classifier():
with open('poker_data_train.csv', 'rb') as training_data:
	classifier = natural_language_classifier.create(
		training_data = training_data,
		name = 'poker_data_train',
		language = 'en'
		)
print(json.dumps(classifier, indent=2))

#def get_status():
status = natural_language_classifier.status('cedf17x168-nlc-2626')
print(json.dumps(status, indent=2))


if status['status'] == 'Available':
    classes = natural_language_classifier.classify('cedf17x168-nlc-2626',
                                                   'I choose to fold')
    print(json.dumps(classes, indent=2))

def find_class():
	classes = natural_language_classifier.classify('poker_data_train', 'I am going to fold')
	print(json.dumps(classes, indent = 2))


