from flask import Flask, url_for, render_template, request
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import json

# Set the URL for the summarization endpoint
url = "http://localhost:8000/summarize/"

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/summarize', methods=['GET', 'POST'])
def summarize():
    output_data=json.loads("{}")
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        # SUMMARIZATION
        # Set the input data for the request
        input_data = {
            "input": rawtext
        }

        # Send a POST request with JSON data
        response = requests.post(url, json=input_data)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            output_data = response.json()
            
            # Print or use the output data as needed
            print("Final Summary:", output_data.get("output"))
        else:
            print("Error:", response.status_code)
            print(response.text)

    return render_template('index.html', output=output_data.get("output"))

@app.route('/report',methods=['GET'])
def report():
    return render_template("MedTitleGen.html")
   
# GET DATA FROM URL
def get_text(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, "lxml")
    fetched_text = ' '.join(map(lambda p: p.text.soup.find_all('p')))
    return fetched_text


if __name__ == '__main__':
    app.run(debug=True)
