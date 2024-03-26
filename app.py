from flask import Flask, render_template, request, jsonify
from functions import response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    bot_response = response(user_message)

    return jsonify({'message': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
