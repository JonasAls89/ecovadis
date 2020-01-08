from flask import Flask, request, jsonify, Response
import json
import requests
import os
import sys
from processing.feature import dict_merger, get_token
from sesamutils import VariablesConfig, sesam_logger

app = Flask(__name__)
logger = sesam_logger("Steve the logger", app=app)

## Logic for running program in dev
try:
    with open("helpers.json", "r") as stream:
        env_vars = stream.read()
        #os.environ['username'] = env_vars[19:41]
        #os.environ['password'] = env_vars[61:78]
        #os.environ['base_url'] = env_vars[98:137]
        os.environ['username'] = env_vars[19:34]
        os.environ['password'] = env_vars[54:71]
        os.environ['base_url'] = env_vars[91:122]
except OSError as e:
    logger.info("Using env vars defined in SESAM")

## Helpers
required_env_vars = ['username', 'password', 'base_url']
username = os.getenv('username')
password = os.getenv('password')
base_url = os.getenv('base_url')

payload = {
        'grant_type': "password",
        'username' : username,
        'password' : password
}

headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
}

##Helper function for yielding on batch fetch
def stream_json(entities):
    logger.info("streaming started")
    try:
        first = True
        yield '['
        for i, row in enumerate(entities):
            if not first:
                yield ','
            else:
                first = False
            
            yield json.dumps(row)
        yield ']'
    except Exception as e:
        logger.error(f"Exiting with error : {e}")
    logger.info("stream ended")
##

@app.route('/')
def index():
    output = {
        'service': 'EcoVadis is running',
        'remote_addr': request.remote_addr
    }
    return jsonify(output)

@app.route('/entities/get/<path>', methods=['GET','POST'])
def get_data(path):
    logger.info(f"Ecovadis is running")
    ## Validating env vars
    config = VariablesConfig(required_env_vars)

    if not config.validate():
        sys.exit(1) 

    token = get_token(headers, payload, base_url)

    ## Requesting data
    request_url = f"{base_url}/v2.0/{path}"

    data = requests.get(request_url, headers=token)
    if not data.ok:
        logger.error(f"Unexpected response status code: {data.content}")
        return f"Unexpected error : {data.content}", 500

    try:
        data_transform = json.loads(data.content.decode('utf-8-sig'))
    except IndexError as e:
        logger.error(f"exiting with error {e}")
    except KeyError as e:
        logger.error(f"exiting with error {e}")

    return Response(stream_json(data_transform), mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)