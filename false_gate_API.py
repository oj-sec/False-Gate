#!/usr/bin/env python3

# API interface for False Gate

from flask import Flask, jsonify, request, render_template
import datetime
import browser_driver

app = Flask(__name__, static_url_path='/static')

@app.route("/false_gate/submit_url/", methods=['POST'])
def submit_uri():

	url = request.get_json()['url']

	try:
		credentials = request.get_json()['credentials']
	except KeyError:
		credentials = {"jasonpostman@gmail.com":"bobbytables18#"}

	bd = browser_driver.BrowserDriver(url, credentials)

	results = bd.start()

	if results:

		return results

	else:

		return {}


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
