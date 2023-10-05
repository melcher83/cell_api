#automated cell metric gathering for Peplink modems using API

import keyboard
import requests
from requests.auth import HTTPBasicAuth
import time
import sys
requests.urllib3.disable_warnings()


if __name__ == '__main__':
    #print(sys.argv[0])
    #Parameters
    url='https://' + sys.argv[1] + '/api/' #'https://<ip address>/api/'
    username=sys.argv[2]
    password=sys.argv[3]
    timeout = int(sys.argv[4]) #how long script will run in seconds
    interval=int(sys.argv[5])  #how often script will poll data in seconds



    #setup API Access
    query = {'username': username, 'password': password}
    peplink = requests.Session()
    response = peplink.post(url + 'login', params=query,verify=False)


    query={'action':'add','name':'client 1','scope':'api'}

    #authentication
    response=peplink.post(url+'auth.client',params=query,verify=False,auth=HTTPBasicAuth(username, password))

    x=response.json()['response']['clientId']
    y=response.json()['response']['clientSecret']

    query={'clientId':x,'clientSecret':y}

    response=peplink.post(url+'auth.token.grant',params=query,verify=False)


    a_token=response.json()['response']['accessToken']
    my_headers = {'token': x}

    #variables
    rssi=[]
    sinr=[]
    rsrp=[]
    rsrq=[]

    timeout_start = time.time()
    response = peplink.get(url + 'status.wan.connection', headers=my_headers)
    #print(response.json()['response']['2']['cellular']['rat'][0]['band'][0]['signal'])
    # Gather Data
    while time.time() < timeout_start +timeout:
        test = 0
        if test == 5:
            break

        if keyboard.is_pressed('q'):
            break
        test -= 1
        response = peplink.get(url + 'status.wan.connection', headers=my_headers)
        rssi.append(response.json()['response']['2']['cellular']['rat'][0]['band'][0]['signal']['rssi'])
        sinr.append(response.json()['response']['2']['cellular']['rat'][0]['band'][0]['signal']['sinr'])
        rsrp.append(response.json()['response']['2']['cellular']['rat'][0]['band'][0]['signal']['rsrp'])
        rsrq.append(response.json()['response']['2']['cellular']['rat'][0]['band'][0]['signal']['rsrq'])
        print(str(round(time.time()-(timeout_start+timeout)))+' seconds remaining')
        time.sleep(interval)

    response = peplink.get(url + 'info.location', headers=my_headers)
    latitude=response.json()['response']['location']['latitude']
    longitude=response.json()['response']['location']['longitude']
    elevation = response.json()['response']['location']['altitude']

    #remove API Access
    query={'action':'remove','clientId':x}

#
#
#
    response=peplink.post(url+'auth.client',params=query,verify=False)
#Process Data
#=============================================================
    sum=0

    i=0

    while i<len(rssi):
        sum=sum+rssi[i]
        i=i+1

    rssi_avg=sum/len(rssi)
#============================================================
    sum = 0

    i = 0

    while i < len(sinr):
        sum = sum + sinr[i]
        i = i + 1
    sinr_avg = sum / len(sinr)

#=============================================================
    sum = 0

    i = 0

    while i < len(rsrp):
        sum = sum + rsrp[i]
        i = i + 1


    rsrp_avg=sum/len(rsrp)
#==============================================================

    sum = 0

    i = 0

    while i < len(rsrq):
        sum = sum + rsrq[i]
        i = i + 1

    rsrq_avg = sum / len(rsrq)
#Display Data
    print('RSSI AVG: '+ str(rssi_avg) + '  ' + str(len(rsrq)) + ' samples')
    print('SINR AVG: ' + str(sinr_avg)+ '  ' + str(len(rsrq)) + ' samples')
    print('RSRP AVG: ' + str(rsrp_avg)+ '  ' + str(len(rsrq)) + ' samples')
    print('RSRQ AVG: ' + str(rsrq_avg)+ '  ' + str(len(rsrq)) + ' samples')
    print('Latitude: ' + str(latitude) + "     Longitude:  " + str(longitude) + "    Elevation:  " + str(elevation))
#
#
