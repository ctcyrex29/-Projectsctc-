from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(_name_)

@app.route("/webhook", methods=["POST"])

def webhook():
	incoming_message = request.value.get("Body", "").lower()
	response = MessagingResponse()
	message = response.message()

	if incoming_message == "hello":
		message.body("hello! How can l help you?")
	else:
		message.body("l'm sorry, l couldn't understand your message.")

	return str(response)

if_name_=="_main_"
app.run()