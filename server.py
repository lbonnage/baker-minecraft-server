from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from pprint import pprint
import googleapiclient.discovery
import configuration
import os

app = Flask(__name__)
CORS(app)


def retrieve_ip(compute, project, zone):
	instances = compute.instances().list(project=project, zone=zone).execute()['items']
	for instance in instances:
		# Search for the desired server instance
		if instance['name'] == 'mc-server':
			return instance['networkInterfaces'][0]['accessConfigs'][0]['natIP']


def start_google_server():

	# Set the authentication credential environment variable to the path to our key file
	os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = configuration.KEY_FILE

	compute = googleapiclient.discovery.build('compute', 'v1')

	# Start the instance
	request = compute.instances().start(project=configuration.PROJECT_ID, zone=configuration.ZONE, instance=configuration.INSTANCE_NAME)
	response = request.execute()

	pprint(response)

	externalip = retrieve_ip(compute, configuration.PROJECT_ID, configuration.ZONE)
	print(externalip)
	return externalip


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

	message = '[Server] Password Incorrect'
	ip_address = 'Password incorrect'

	if inputted_password == configuration.SERVER_PASSWORD:
		ip_address = start_google_server()
		message = '[Server] Successfully started server with IP: ' + ip_address

	return


app.run()
