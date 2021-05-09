import cv2
import urllib.request
import time

octo_api_token = '<YOUR_TOKEN_HERE>'

detector = cv2.QRCodeDetector()


while True:
    #Get snapshot
    urllib.request.urlretrieve('http://192.168.1.118/webcam/?action=snapshot', 'snapshot.jpeg')
    time.sleep(1)
    #cam = cv2.VideoCapture('http://192.168.1.118/webcam/?action=stream')
    #_, img = cam.read()

    img = cv2.imread('snapshot.jpeg')
    #detect QR codes
    data, bbox, _ = detector.detectAndDecode(img)

    #if QR code:
    if data:
        #Change filament to QR code if exists
        print("QR Code detected-->", data)

        #Confirmation beep

        #Else create new filament
        #Confirmation beep

    #cv2.imshow("img", img)
    #if cv2.waitKey(1) == ord("Q"):
    #    break

    time.sleep(1)

#cam.release()
cv2.destroyAllWindows()

    #If error
        #Error beep

