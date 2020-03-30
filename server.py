from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from pprint import pprint
import googleapiclient.discovery
import configuration
import os

app = Flask(__name__)
CORS(app)


##
# Retrieves the IP address for the started server
##
def retrieve_ip(compute, requested_server):
	instances = compute.instances().list(project=configuration.PROJECT_ID, zone=configuration.ZONE).execute()['items']
	for instance in instances:
		# Search for the desired server instance
		if instance['name'] == requested_server:
			return instance['networkInterfaces'][0]['accessConfigs'][0]['natIP']


##
# Initializes the desired server
##
def start_server(requested_server):

	# Set the authentication credential environment variable to the path to our key file
	os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = configuration.KEY_FILE

	compute = googleapiclient.discovery.build('compute', 'v1')

	# Start the instance
	start_request = compute.instances().start(project=configuration.PROJECT_ID, zone=configuration.ZONE, instance=requested_server)
	response = start_request.execute()

	pprint(response)

	external_ip = retrieve_ip(compute, requested_server)
	return external_ip


##
# Endpoint for loading the website homepage
##
@app.route("/")
def load_index():
	return render_template('index.html')


##
# Receives the request to initialize the server.
# If the password is correct and the server isn't running, starts the server.
# If the password is correct and the server is running, returns the IP address.
# If the password is incorrect, returns a fail message to the browser.
##
@app.route('/init_server', methods=['POST'])
def init_server():

	inputted_password = request.form['password']
	requested_server = request.form['server']

	message = 'Password incorrect.'

	if requested_server == '':
		message = 'Please select a server from the dropdown list.'
	elif inputted_password == configuration.PASSWORD:
		ip_address = start_server(requested_server)
		message = 'Successfully started server \"' + requested_server + '\" with IP: ' + ip_address
	elif inputted_password in configuration.BAKER_TROPES:
		message = 'Password incorrect.  Nice Baker reference though!'

	return render_template('index.html', ipMessage=message)


if __name__ == '__main__':
	# This is used when running locally. Gunicorn is used to run the
	# application on Google App Engine. See entrypoint in app.yaml.
	app.run(host='127.0.0.1', port=8080, debug=True)
