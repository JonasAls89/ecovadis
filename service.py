from flask import Flask, request, jsonify, Response
import json
import requests
import logging
import os
import sys
from processing.feature import dict_merger
from sesamutils import VariablesConfig 

app = Flask(__name__)

username = os.getenv('username')
password = os.getenv('password')

logger = None

required_env_vars = ['username', 'password']

@app.route('/')
def index():
    output = {
        'service': 'EcoVadis is running',
        'remote_addr': request.remote_addr
    }
    return jsonify(output)

@app.route('/entities/get', methods=['GET','POST'])
def get_data():
    app.logger.info(f"Ecovadis is running")
    ## Validating env vars
    ##check_env_variables(required_env_vars, missing_env_vars)
    config = VariablesConfig(required_env_vars)

    if not config.validate():
        sys.exit(1)

    ##if len(missing_env_vars) != 0:
    ##    app.logger.error(f"Missing the following required environment variable(s) {missing_env_vars}")
    ##    sys.exit(1)
    ##

    request_body = request.get_json()

    payload = {
        'username' : username,
        'password' : password,
    }    

    ## Generating token and checking response
    generate_url = "https://www.james.com"
    check_response = requests.get(generate_url)
    if not check_response.ok:
        app.logger.error(f"Access token request failed. Error: {check_response.content}")
        raise
    valid_response = check_response.json()
    token = {'Authorization' : 'Bearer ' + valid_response['token']}
    ##

    ## Requesting data
    request_url = f"https://services.com"
    #app.logger.info(request_url)
    data = requests.get(request_url, headers=token)
    if not data.ok:
        app.logger.error(f"Unexpected response status code: {data.content}")
        return f"Unexpected error : {data.content}", 500
        raise
    #app.logger.info(f"returning call with status code {data.json()}")
    try:
        data_transform = data.json()['features'][0]
        data_transform["data"] = data_transform.pop("attributes")
    except IndexError as e:
        app.logger.error(f"exiting with error {e}")
        data_transform = default_response
    except KeyError as e:
        app.logger.error(f"exiting with error {e}")
        data_transform = default_response

    sesam_dict = dict_merger(dict(request_body[0]), dict(data_transform))
    ##

    return Response(json.dumps(sesam_dict), mimetype='application/json')

if __name__ == '__main__':
    # Set up logging
    format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logger = logging.getLogger('EcoVadis Wabbalabbadabdab')

    # Log to stdout
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(logging.Formatter(format_string))
    logger.addHandler(stdout_handler)

    logger.setLevel(logging.DEBUG)
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)