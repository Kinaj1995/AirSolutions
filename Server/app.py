
from flask import Flask, render_template


import time



app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/sensors', methods=['GET'])
def sensors():
    return render_template('index.html')

@app.route('/admin', methods=['GET'])
def admin():
    return render_template('index.html')







#--Starts the Server
if(__name__ == "__main__"):
    app.run(debug=True)