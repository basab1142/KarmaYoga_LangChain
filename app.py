from flask import Flask, render_template, request, jsonify
from functions import response, gemini_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/gemini.html')
def gem():
    return render_template('gemini.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    bot_response = response(user_message)

    return jsonify({'message': bot_response})

@app.route('/api/chat2', methods=['POST'])
def chat2():
    user_message = request.json.get('message')

    bot_response = gemini_response(user_message)

    return jsonify({'message': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
