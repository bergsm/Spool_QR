import cv2
import json
import urllib.request
import time
import requests

octo_url = 'http://192.168.1.118'
octo_api_token = '<YOUR_TOKEN_HERE>'

octo_headers = {
        'Content-Type': 'application/json',
        'X-Api-Key': octo_api_token
        }


detector = cv2.QRCodeDetector()


while True:
    #Get snapshot
    #urllib.request.urlretrieve('http://192.168.1.118/webcam/?action=snapshot', 'snapshot.jpeg')
    urllib.request.urlretrieve(octo_url + '/webcam/?action=snapshot', 'snapshot.jpeg')
    time.sleep(0.3)
    #cam = cv2.VideoCapture('http://192.168.1.118/webcam/?action=stream')
    #_, img = cam.read()

    img = cv2.imread('snapshot.jpeg')
    #detect QR codes
    data, bbox, _ = detector.detectAndDecode(img)

    #response = requests.post(octo_url+'/api/printer/command', headers=octo_headers, data=json.dumps({'command': 'M300 P500'}))
    #print(response)
    #print(response.text)



    #if QR code:
    if data:
        #Change filament to QR code if exists
        print("QR Code detected-->", data)
        response = requests.post(octo_url+'/api/printer/command', headers=octo_headers, data=json.dumps({'command': 'M300 P500'}))

        time.sleep(10)

        #Confirmation beep

        #Else create new filament
        #Confirmation beep

    #cv2.imshow("img", img)
    #if cv2.waitKey(1) == ord("Q"):
    #    break

    time.sleep(0.5)

#cam.release()
cv2.destroyAllWindows()

    #If error
        #Error beep

