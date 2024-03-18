from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

data_dir = 'data'

# Route to get all tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = []

    # Iterate over JSON files in the data directory
    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(data_dir, filename)
            with open(file_path, 'r') as file:
                task_data = json.load(file)
                tasks.append(task_data)
    return jsonify(tasks)

# Route to get a specific task by ID
@app.route('/api/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = next((task for task in tasks if task['id'] == id), None)
    if task:
        return jsonify(task)
    else:
        return jsonify({"message": "task not found"}), 404

# Function to write task data to a JSON file
def write_task_to_json(task_data):
    # Generate a unique filename for the new JSON file
    file_name = f"task_{len(os.listdir(data_dir)) + 1}.json"
    file_path = os.path.join(data_dir, file_name)

    # Write book data to the JSON file
    with open(file_path, 'w') as file:
        json.dump(task_data, file)

@app.route('/api/tasks', methods=['POST'])
def add_book():
    # Get book data from the request
    task_data = request.json
    
    # Write book data to a JSON file
    write_task_to_json(task_data)

    return jsonify({'message': 'Task added successfully'})

if __name__ == '__main__':
    app.run(debug=True)
