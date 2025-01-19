from flask import Flask, request, jsonify
from allosaurus.app import read_recognizer

app = Flask(__name__)

@app.route('/', methods={'GET'})
def hello():
    return "Hello, Flask Server!\n"


@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        data = request.get_json()  # Expecting JSON data
        # Extract 'text' from JSON payload
        audio = data.get('audio', '')
        print(f"Received audio: {audio}")
        # You can add additional processing here if needed
        response = {"status": "success"}
    except Exception as e:
        print(f"Error: {e}")
        response = {"status": "error", "message": str(e)}

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Adjust the port as needed