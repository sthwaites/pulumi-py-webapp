from flask import Flask, render_template
import os

app = Flask(__name__)

msg = os.environ.get('MESSAGE')

@app.route('/')
def index():
    return render_template('index.html', msg=msg)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
