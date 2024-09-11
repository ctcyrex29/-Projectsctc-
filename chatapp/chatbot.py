import requests
import json

def generate_access_token(phone_number, country_code):
	self.access_token = ...
	self.chat_ld = ...


class WhatsAppBot:
	def_init_(self, access_token)
	self.access_token = access_token
	self.chat_ld = None
	self.contacts = []



def send_message(self, phone_number, country_code, message):
	request = requests.post("https://api.whatsapp.com/send?phone=" + phone_number + "&country=" + country_code + "&text=" + message, headers={})

def receive_message(self, phone_number, country_code):
	request = requests.get("https://api.whatsapp.com/send_receive/message?phone=" + phone_number + "&country=" + country_code)
	chat_ld = request.json()['chat']['id']
	message = request

def create_chat(self, phone_number, country_code):
	request = requests.post("https://api.whatsapp.com/send=" + phone_number + "&country=" + country_code)
	chat_ld = request.json()['chat']['id']
	return chat

def add_contact(self, phone_number):
	request = requests.post("https://api.whatsapp.com/send?phone=" + phone_number + "&country=" + country_code)
	chat_ld = request.json()['chat']['id']
	confirmation = "your contact was added successfully!"

def run_whatsappbot():
	access_token = generate_access_token("0713547520", "Zimbabwe")
	while true:
	run_whatsappbot()

