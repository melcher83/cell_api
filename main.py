# This is a sample Python script.
import json

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
from requests.auth import HTTPBasicAuth
import time

requests.urllib3.disable_warnings()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':


    url='https://192.168.50.1/api/'
    username='admin'
    password='Private123'
    timeout = 300
    timeout_start = time.time()
    query = {'username': username, 'password': password}
    peplink = requests.Session()
    response = peplink.post(url + 'login', params=query,verify=False)
    #print(response.json())

    # my_headers={'token':'3ed00898f47a4e40753838c8eda69a62','Cookie':'bauth=usBg7D8wVdJrgDiFUOB8VzSeaPmRZMdifQymtwLfLvFT2'}
    # # print request object
    #print(response.json())
    #
    #
    #response = requests.get(url+'status.wan.connection',auth=HTTPBasicAuth(username,password) , verify=False)
    #
    # # print request object
    # print(response.json())
    query={'action':'add','name':'client 1','scope':'api'}

    response=peplink.post(url+'auth.client',params=query,verify=False,auth=HTTPBasicAuth(username, password))
    #print(response.json())
    x=response.json()['response']['clientId']
    y=response.json()['response']['clientSecret']
    #print(x)
    query={'clientId':x,'clientSecret':y}

    response=peplink.post(url+'auth.token.grant',params=query,verify=False)
    #print(response.json())

    a_token=response.json()['response']['accessToken']
    my_headers = {'token': x}

    rssi=[]
    sinr=[]
    rsrp=[]
    rsrq=[]

    while time.time() < timeout_start +timeout:
        test = 0
        if test == 5:
            break
        test -= 1
        response = peplink.get(url + 'status.wan.connection', headers=my_headers)
        rssi.append(response.json()['response']['2']['cellular']['band'][0]['signal']['rssi'])
        sinr.append(response.json()['response']['2']['cellular']['band'][0]['signal']['sinr'])
        rsrp.append(response.json()['response']['2']['cellular']['band'][0]['signal']['rsrp'])
        rsrq.append(response.json()['response']['2']['cellular']['band'][0]['signal']['rsrq'])
        print(str(round(time.time()-(timeout_start+timeout)))+' seconds remaining')
        time.sleep(15)


    # response=peplink.get(url+'status.wan.connection',headers=my_headers)
    # print(response.json())



    query={'action':'remove','clientId':x}




    response=peplink.post(url+'auth.client',params=query,verify=False)
    #print(response.json())
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

    print('RSSI AVG: '+ str(rssi_avg))
    print('SINR AVG: ' + str(sinr_avg))
    print('RSRP AVG: ' + str(rsrp_avg))
    print('RSRQ AVG: ' + str(rsrq_avg))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
