from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Function to load diseases from the JSON file
def load_diseases_from_json():
    # Check if the file exists
    if not os.path.exists('diseases.json'):
        return []
    
    # Read data from the file
    with open('diseases.json', 'r') as file:
        try:
            data = json.load(file)
            return data.get('diseases', [])
        except json.JSONDecodeError:
            return []  # Return empty if JSON is invalid

# Function to diagnose based on symptoms
def diagnose(symptoms, diseases_db):
    matched_diseases = []

    print("Symptoms provided:", symptoms)  # Debugging: print the symptoms being received

    for disease in diseases_db:
        disease_symptoms = disease['symptoms']
        print(f"Checking disease: {disease['name']} with symptoms: {disease_symptoms}")  # Debugging: print the disease symptoms

        matches = set(symptoms) & set(disease_symptoms)
        print(f"Matches found: {matches}")  # Debugging: print matching symptoms

        if matches:
            matched_diseases.append((disease['name'], len(matches), disease))

    matched_diseases.sort(key=lambda x: x[1], reverse=True)

    if not matched_diseases:
        print("No matches found.")
        return "No matching diseases found based on the input symptoms."

    result = []
    for disease, match_count, full_disease in matched_diseases:
        disease_info = {
            "name": disease,
            "matched_symptoms": match_count
        }
        
        # Include causes and medications only if they are not empty
        if full_disease['causes']:
            disease_info['causes'] = full_disease['causes']
        if full_disease['medications']:
            disease_info['medications'] = full_disease['medications']

        result.append(disease_info)
    
    print("Diagnosis result:", result)  # Debugging: print the final result
    return result

@app.route('/diagnose', methods=['POST'])
def diagnose_disease():
    data = request.get_json()  # Get the input data (symptoms)
    symptoms = data.get('symptoms', [])
    
    if not symptoms:
        return jsonify({"error": "No symptoms provided."}), 400

    diseases_db = load_diseases_from_json()

    if not diseases_db:
        return jsonify({"error": "Disease database is empty or missing."}), 500

    diagnosis_result = diagnose(symptoms, diseases_db)
    
    if isinstance(diagnosis_result, str):
        return jsonify({"message": diagnosis_result}), 200
    
    return jsonify(diagnosis_result)

if __name__ == '__main__':
    # Run the app on all available interfaces to be accessible externally if needed
    app.run(host='0.0.0.0', port=5000, debug=True)
