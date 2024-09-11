import json
from difflib import get_close_matches
from typing import List
import pyttsx3
import speech_recognition as sr
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from serial import Serial
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QInputDialog

def control_light(ser: Serial, action: str):
    """Sends commands to Arduino to control the light."""
    if action == "on":
        ser.write(b"1")  # Send "1" to turn on the light
        print("Bot: Light turned on.")
        speak("The light is turned on.")
    elif action == "off":
        ser.write(b"0")  # Send "0" to turn off the light
        print("Bot: Light turned off.")
        speak("The light is turned off.")
    else:
        print("Bot: I'm sorry, I didn't understand the command.")



def get_answer_for_question(question: str, knowledge_base: dict) -> str:
    """Retrieves the answer for the given question from the knowledge base."""
    for qna in knowledge_base["questions"]:
        if qna["question"].lower() == question.lower():
            return qna["answer"]
    return "I'm sorry, I don't have an answer for that question."

def find_bestmatch(input_str: str, options: List[str]) -> str:
    """Finds the best match for the given input string from a list of options."""
    close_matches = get_close_matches(input_str, options, n=1, cutoff=0.8)
    if close_matches:
        return close_matches[0]
    else:
        return ""

def load_knowledge_base(filename: str) -> dict:
    """Loads the knowledge base from a JSON file."""
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"questions": []}

def save_knowledge_base(filename: str, knowledge_base: dict):
    """Saves the knowledge base to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(knowledge_base, file, indent=4)
def chatbot():
    """Main function for the chatbot."""
    knowledge_base = load_knowledge_base('knowledge_base.json')
    arduino_port = "COM 4"  # Replace with the correct port for your Arduino
    arduino_baudrate = 9600

    try:
        ser = Serial(arduino_port, arduino_baudrate)
        print("Bot: Arduino connected.")
        speak("Arduino connected.")
    except Exception as e:
        print(f"Bot: Failed to connect to Arduino: {str(e)}")
        speak("Failed to connect to Arduino.")

    while True:
        user_input = input('You: ')

        if user_input.lower() == 'quit':
            break

        if user_input.lower() == 'turn on the light':
            control_light(ser, "on")
        elif user_input.lower() == 'turn off the light':
            control_light(ser, "off")
        else:
            best_match = find_bestmatch(user_input, [q["question"] for q in knowledge_base["questions"]])

            if best_match:
                answer = get_answer_for_question(best_match, knowledge_base)
                print(f'Bot: {answer}')
                speak(answer)  # Convert the answer to speech
            else:
                print('Bot: I don\'t know the answer. Can you teach me?')
                new_answer = input('Type the answer or "skip" to skip: ')
                if new_answer.lower() != 'skip':
                    knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                    save_knowledge_base('knowledge_base.json', knowledge_base)
                    print('Bot: Thank you for teaching me a new response!')
                    speak('Thank you for teaching me a new response!')

    ser.close()        

def speak(text: str):
    """Converts the given text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen() -> str:
    """Listens to the user's voice command and returns the recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

class ChatbotGUI(QMainWindow):
    def __init__(self, knowledge_base):
        super().__init__()
        self.knowledge_base = knowledge_base
        self.setWindowTitle("Chatbot")

        self.label = QLabel("You:", self)
        self.label.move(20, 20)

        self.input_box = QLineEdit(self)
        self.input_box.setGeometry(80, 20, 300, 30)

        self.btn_send = QPushButton("Send", self)
        self.btn_send.setGeometry(400, 20, 80, 30)
        self.btn_send.clicked.connect(self.send_message)

        self.btn_listen = QPushButton("Listen", self)
        self.btn_listen.setGeometry(400, 60, 80, 30)
        self.btn_listen.clicked.connect(self.listen_command)

        self.output_box = QLabel(self)
        self.output_box.setGeometry(20, 100, 460, 160)
        self.output_box.setWordWrap(True)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input_box)
        self.layout.addWidget(self.btn_send)
        self.layout.addWidget(self.btn_listen)
        self.layout.addWidget(self.output_box)

        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def listen_command(self):
        command = listen()
        self.input_box.setText(command)

        self.output_box = QLabel(self)
        self.output_box.setGeometry(20, 100, 460, 160)
        self.output_box.setWordWrap(True)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input_box)
        self.layout.addWidget(self.btn_send)
        self.layout.addWidget(self.btn_listen)
        self.layout.addWidget(self.output_box)

        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)
    def send_message(self):
        user_input = self.input_box.text()
        self.input_box.clear()

        if user_input.lower() == 'quit':
            QApplication.quit()

        best_match = find_bestmatch(user_input, [q["question"] for q in self.knowledge_base["questions"]])

        if best_match:
            answer = get_answer_for_question(best_match, self.knowledge_base)
            self.display_message(f'Bot: {answer}')
            speak(answer)  # Convert the answer to speech
        else:
            self.display_message('Bot: I don\'t know the answer. Can you teach me?')
            new_answer = self.get_user_input('Type the answer or "skip" to skip:')
            if new_answer.lower() != 'skip':
                self.knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', self.knowledge_base)
                self.display_message('Bot: Thank you for teaching me a new response!')
                speak('Thank you for teaching me a new response!')

    def display_message(self, message):
        current_text = self.output_box.text()
        self.output_box.setText(f'{current_text}\n{message}')

    def get_user_input(self, prompt):
        text, ok_pressed = QInputDialog.getText(self, 'User Input', prompt)
        if ok_pressed:
            return text
        return ""

knowledge_base = {}  # Replace with your knowledge base
app = QApplication([])
window = ChatbotGUI(knowledge_base)
window.show()
app.exec_()
if __name__ == "__main__":
    chatbot()