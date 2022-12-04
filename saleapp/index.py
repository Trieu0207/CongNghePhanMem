from flask import render_template
from saleapp import app
from saleapp.admin import *

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)