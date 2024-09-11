import json
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    """Loads the knowledge base from a JSON file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    """Saves the knowledge base to a JSON file."""
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)

def find_bestmatch(user_question: str, questions: list[str]) -> str | None:
    """Finds the best match for the user question from the list of questions."""
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    """Searches the knowledge base for the answer to a specific question."""
    for entry in knowledge_base["questions"]:
        if entry["question"] == question:
            return entry["answer"]
    return None

def chatbot():
    """Main function for the chatbot."""
    knowledge_base = load_knowledge_base('knowledge_base.json')

    while True:
        user_input = input('You: ')

        if user_input.lower() == 'quit':
            break

        best_match = find_bestmatch(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don\'t know the answer. Can you teach me?')
            new_answer = input('Type the answer or "skip" to skip: ')
            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('Bot: Thank you for teaching me a new response!')

if __name__ == '__main__':
    chatbot()
