import uuid
import requests
import datetime
import json
import random
import time
import sys


def run(env,username,days,goal,percent_num):
    #environment
    #env= 'https://stg-api.tidepool.org'
    #env = 'https://qa1.development.tidepool.org'
    #env = 'https://qa2.development.tidepool.org'
    #env = 'https://app.tidepool.org'

    #login and get token and userid
    #num=sys.argv[1]
    #username = 'brian+back2583@tidepool.org'
    password = 'tidepool'
    response = requests.post(env+'/auth/login', auth=(username, password))
    token = response.headers['x-tidepool-session-token']
    userId = response.json()['userid']
    #days=30

    #goal_num = 1
    #percent_num=0.3
    #sp = 0.00004


    sampling_full = True
    sampling_interval = 5 # interval at which a sample is obtained (units defined in date_list)
    sampling_totaltime = (1440*days)
    if sampling_full:
        sampling_totaltime = sampling_totaltime+5 # total time from now to the past to generate samples (units defined in date_list)

    # samples are picked from elements bin according to probabilities distribution for a length of the sample times
    base = datetime.datetime.utcnow() - datetime.timedelta(days = days)
    #base = datetime.datetime(2023,8,1,0,0,0)
    date_list = [base - datetime.timedelta(minutes=x) for x in range(sampling_interval,sampling_totaltime,sampling_interval)] 
    date_list = [dl.strftime('%Y-%m-%dT%H:%M:%S') for dl in date_list] #list of dates from now to the past amount of time defined in sampling_totaltime
    date_list.reverse()


    # function to print the first m multiple
    # of a number n without using loop.
    def multiple(m, n):
    
        # inserts all elements from n to
        # (m * n)+1 incremented by n.
        a = range(n, (m * n)+1, n)
        return a
    start = [0]
    start.extend(multiple(days*24,12))

    #start = [0 , 288*2, 288*5,288*8,288*11,288*14 ]

    # open a new continuous session

    headers = {
        'x-tidepool-session-token': token,
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
    }

    json_data = {
        'deduplicator': {
            'name': 'org.tidepool.deduplicator.dataset.delete.origin',
            'version': '1.0.0',
        },
        'type': 'upload',
        'client': {
            'name': 'org.tidepool.mobile',
            'version': '2.1.8',
        },
        'dataSetType': 'continuous',
    }


    response = requests.post(env+'/v1/users/'+userId+'/datasets', headers=headers, json=json_data)

    sessionId = response.json()['data']['id']

    # create a data array to upload


    data ={
        "id": "01ae128094e9d0b6fa5348d1765b2ad2",
        "origin": {
            "id": "FC70765C-1DEA-4DD7-8D0B-5FF63CB0FF3B",
            "name": "com.apple.HealthKit",
            "payload": {
                "device": {
                    "manufacturer": "Dexcom",
                    "model": "G6",
                    "name": "CGMBLEKit",
                    "softwareVersion": "21.0",
                    "udiDeviceIdentifier": "00386270000385"
                },
                "sourceRevision": {
                    "operatingSystemVersion": "15.4.1",
                    "productType": "iPhone14,2",
                    "source": {
                        "bundleIdentifier": "com.PQPNNRRFUC.loopkit.Loop",
                        "name": "Loop"
                    },
                    "version": "57"
                }
            },
            "type": "service"
        },
        "payload": {
            "HKMetadataKeySyncIdentifier": "8TWG40 758174",
            "HKMetadataKeySyncVersion": 1,
            "com.LoopKit.GlucoseKit.HKMetadataKey.GlucoseTrend": "\u2191",
            "com.LoopKit.GlucoseKit.HKMetadataKey.GlucoseTrendRateUnit": "mg/min\u00b7dL",
            "com.LoopKit.GlucoseKit.HKMetadataKey.GlucoseTrendRateValue": 2.8
        },
        "time": "2022-06-18T17:43:37.000Z",
        "type": "cbg",
        "units": "mmol/L",
        "uploadId": "52e9a41e804e2c5cd788ea3cf8fbd9c5",
        "value": 3.21597
    }





    elements = [0,3, 3.9,10,13.9]
    values = [x+0.5 for x in elements]
    verylow = values[0]
    low = values[1]
    target = values[2]
    high = values[3]
    veryhigh = values[4]
    ranges = [0,0,0,0,0]
    labels=['verylow','low','target','high','veryhigh']
    #values = values[:-1]
    headers = {
            'x-tidepool-session-token': token,
            # Already added when you pass json=
            # 'Content-Type': 'application/json',
        }
    #last 24 hours  
    json_list =[]
    for j in range(days*24):
    #for j,v in enumerate(range(1)):
        #upid = uuid.uuid4().hex
        #percent_num=random.uniform(0.5, 0.9)
        if j>=0:
            value = verylow
            percent = percent_num
            value_index=0
            pvalue = target
            ppercent = 1-percent
            pvalue_index = 2
        
    
        
            



        for i,da in enumerate(date_list[start[j]:start[j+1]]):
            
            
            if  ranges[value_index] / (1+sum(ranges))< percent and sum(ranges)/len(date_list[0:start[j+1]])<goal:


                data["time"]  = da+'.000Z'
                data["id"] = uuid.uuid4().hex
                data["origin"]["id"] = uuid.uuid4().hex
                #data["uploadId"] =  upid
                data["value"] = value
                ranges[value_index] = ranges[value_index] +1
                json_list.append(dict(data))

                #name = input('Type enter to continue')
                
                if len(json_list) == 100 or i==len(date_list[start[j]:start[j+1]])-1:
                    #time.sleep(1)
                #ranges_list = zip(labels,ranges)  
                #print(sessionId)
                #print(json_list[-1]["time"],list(ranges_list))
                    response = requests.post(env+'/dataservices/v1/datasets/'+sessionId+'/data', headers=headers, json=json_list)

                    #print(i,response)
                    json_list = []
            elif sum(ranges)/len(date_list[0:start[j+1]])<goal:
                data["time"]  = da+'.000Z'
                data["id"] = uuid.uuid4().hex
                data["origin"]["id"] = uuid.uuid4().hex
                #data["uploadId"] =  upid
                data["value"] = pvalue
                ranges[pvalue_index] = ranges[pvalue_index] +1
                json_list.append(dict(data))

                #name = input('Type enter to continue')
                
                if len(json_list) == 100 or i==len(date_list[start[j]:start[j+1]])-1: 

                    #time.sleep(1)
                #ranges_list = zip(labels,ranges)  
                #print(sessionId)
                #print(json_list[-1]["time"],list(ranges_list))
                
                    response = requests.post(env+'/dataservices/v1/datasets/'+sessionId+'/data', headers=headers, json=json_list)

                    #print(i,response)
                    json_list = []
            rsum = sum(ranges)
        if j==((days*24)-1):
            print(username,j,[r/rsum for r in ranges ],ranges,len(date_list[0:start[j+1]]), sum(ranges)/len(date_list[0:start[j+1]]))
        
        
        #time.sleep(60)
        #response = requests.post(env+'/auth/login', auth=(username, password))
        #token = response.headers['x-tidepool-session-token']
        #headers = {
        #'x-tidepool-session-token': token,
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
        #}
        #response = requests.post(env+'/v1/users/'+userId+'/datasets', headers=headers, json=json_data)
        #sessionId = response.json()['data']['id']


                    
        # if len(json_list)>0:
        #         #time.sleep(1)

        #         ranges_list = zip(labels,ranges)  
        #         print(json_list[-1]["time"],list(ranges_list))
        #         response = requests.post(env+'/dataservices/v1/datasets/'+sessionId+'/data', headers=headers, json=json_list)

        #         print(response)
        #         json_list = []







