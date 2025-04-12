from flask import Flask, request, jsonify
from ago import process_energy_file, handle_sustainability_goal, generate_response
from vtracker import df  # Assuming `vtracker.py` has loaded the DataFrame

app = Flask(__name__)

@app.route('/api/sustainability_goal', methods=['POST'])
def set_sustainability_goal():
    data = request.json  # Receive data from frontend
    choice = data.get('choice')
    response = handle_sustainability_goal()
    return jsonify({'message': response})

@app.route('/api/energy_bill', methods=['POST'])
def process_energy_bill():
    file_content = request.json.get('file_content')
    file_path = 'temp_energy_bill.json'  # Save content temporarily
    with open(file_path, 'w') as f:
        f.write(file_content)
    result = process_energy_file(file_path)
    return jsonify(result)

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    analysis = request.json.get('analysis')
    response = generate_response(f"Based on analysis: {analysis}\nProvide recommendations.")
    return jsonify({'recommendations': response})

@app.route('/api/vtracker_data', methods=['GET'])
def get_vtracker_data():
    # Convert DataFrame to JSON for visualization
    data = df.to_dict(orient='records')
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)