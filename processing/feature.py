import os
import requests

## Merge helper function
def dict_merger(dict1, dict2): 
    res = {**dict1, **dict2} 
    return res


## Generating token and checking response
def get_token(headers, payload):
    check_response = requests.get("https://api-sandbox.ecovadis-survey.com/EVToken", headers=headers, data=payload)
    if not check_response.ok:
        app.logger.error(f"Access token request failed. Error: {check_response.content}")
        raise
    valid_response = check_response.json()
    token = {'Authorization' : 'Bearer ' + valid_response['access_token']}
    return token