import requests
from requests.auth import HTTPBasicAuth
import json
import yaml

url = 'https://heredev.service-now.com/api/now/v1/table/sc_req_item?short_description=Submit requests for AWS Direct Connections'
creds = open("creds.yaml", "r")
user, pswd = yaml.load(creds)
response = requests.get(url, auth=HTTPBasicAuth(user, pswd))
#print response.status_code
items = json.loads(response.text)['result']

i = 0
while i < len(items):
    ritm = items[i]['number']
    print ritm

    response = requests.get('https://heredev.service-now.com/api/here/ritm_variables_api', headers={"RITM": ritm}, auth=HTTPBasicAuth(user, pswd))
    #print response.status_code
    submitted_data = json.loads(response.text)['result'][ritm]
    print "  Requestor_email=" + submitted_data['Requestor_email']
    print "  aws_account=" + submitted_data['u_aws_account']

    response = requests.get('https://heredev.service-now.com/api/now/v1/table/u_nss_ssp_vpc_requests?u_ritm=%s' % ritm, auth=HTTPBasicAuth(user, pswd))
    #print response.status_code
    nss_details = json.loads(response.text)['result'][0] # Is it always a list of length 1
    print "  room_id=" + nss_details['u_room_id']

    i += 1


