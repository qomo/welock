import time
import json
import httplib

def DEALdata(value):  #value is int or float of Python's type.
        tempdeal = time.localtime()
        newtime = str(tempdeal[0]) + '-' + str(tempdeal[1]) + '-' + str(tempdeal[2]) + 'T' + str(tempdeal[3]) +':' + str(tempdeal[4]) + ':' + str(tempdeal[5])
        data = {
                "timestamp":newtime,
                "value":value
                }
        return json.JSONEncoder().encode(data)
        
def upload(deviceID,sensorID,value):
        yeelink = 'http://api.yeelink.net/v1.0/device/' + deviceID +'/sensor/' + sensorID + '/datapoints'
        headerdata = {'U-ApiKey': Myapikey}
        data_upload = DEALdata(value)
        conn = httplib.HTTPConnection('api.yeelink.net')
        conn.request(method='POST',url=yeelink,body = data_upload,headers = headerdata) 
        response = conn.getresponse()
        if response.reason == 'OK':
                print 'Data has been uploaded!'
        else:
                print 'Upload faild!'
                print response.reason

Myapikey = '56a0a6abac1515d8fba7b65d170fd0d3'
deviceID = '19669'
sensorID = '34503'

upload(deviceID, sensorID, 1)