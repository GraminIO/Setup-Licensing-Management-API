from flask import Flask, request, redirect, render_template
import json


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home/index.html')


if __name__ == '__main__':
    app.run()

