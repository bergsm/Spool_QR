import cv2
import json
import urllib.request
import time
import requests

octo_url = 'YOUR.IP.ADDRESS'
octo_api_token = '<YOUR_TOKEN_HERE>'


octo_headers = {
        'Content-Type': 'application/json',
        'X-Api-Key': octo_api_token
        }


detector = cv2.QRCodeDetector()

class Filament:
    color = 'White'
    capacity = 1000
    material = 'PLA'
    vendor = 'Amazon'


while True:
    response = requests.get(octo_url+'/api/printer', headers=octo_headers)
    state = response.json()['state']['text']
    print(state)

    if state == "Operational" or state == "Ready":

        #Get snapshot
        urllib.request.urlretrieve(octo_url + '/webcam/?action=snapshot', 'snapshot.jpeg')
        time.sleep(0.3)
        #cam = cv2.VideoCapture('http://192.168.1.118/webcam/?action=stream')
        #_, img = cam.read()

        #TODO read into memory rather than to disk
        img = cv2.imread('snapshot.jpeg')
        #detect QR codes
        data, bbox, _ = detector.detectAndDecode(img)

        #if QR code:
        if data:
            #fetch current spools
            match = False
            response = requests.get(octo_url+'/plugin/filamentmanager/spools', headers=octo_headers)
            print(response)
            print(response.text)
            spools = response.json()

            print("QR Code detected-->", data)
            filament = Filament()
            data = data.split('|')
            print(data)
            filament.color = data[0]
            print(data[0])
            filament.capacity = data[1]
            print(data[1])
            filament.material = data[2]
            print(data[2])
            filament.vendor = data[3]
            print(data[3])

            #Change filament to QR code if exists
            for spool in spools['spools']:
                if filament.color == spool['name']:
                    match = True
                    print('match')
                    spool_id = spool['id']

                    response = requests.patch(octo_url+'/plugin/filamentmanager/selections/0', headers=octo_headers, json={'selection': { 'tool': 0, 'spool': { 'id': spool_id } }, 'updateui': True })
                    print(response)
                    print(response.text)

            #Else create new filament
            if match == False:
                print("New filament")
                response = requests.post(octo_url+'/plugin/filamentmanager/spools', headers=octo_headers, data=json.dumps({'spool': { 'id': None, 'name': filament.color, 'material': filament.material, 'vendor': filament.vendor, 'cost': 20, 'weight': filament.capacity, 'used': 0, 'temp_offset': 0, 'temp_offset': 0, 'profile': { 'id': 1 } }, 'updateui': True }))
                print(response)
                print(response.text)

            if (response.status_code == 200):
                print('Filament changed!')
                #Confirmation beep
                response = requests.post(octo_url+'/api/printer/command', headers=octo_headers, data=json.dumps({'command': 'M300 P50'}))
                time.sleep(0.05)
                response = requests.post(octo_url+'/api/printer/command', headers=octo_headers, data=json.dumps({'command': 'M300 P50'}))
            else:
                print('Error')
                # TODO use bad beep?
                response = requests.post(octo_url+'/api/printer/command', headers=octo_headers, data=json.dumps({'command': 'M300 P3000'}))


            time.sleep(10)

    time.sleep(0.5)

#cam.release()
cv2.destroyAllWindows()

    #If error
        #Error beep

