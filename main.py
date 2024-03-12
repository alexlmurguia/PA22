"""
Subject: Advanced Robotics
Professor: Gilbero Montes

Python script: qrCode scanner.
Reference: https://www.hackster.io/gatoninja236/scan-qr-codes-in-real-time-with-raspberry-pi-a5268b
You can generate qrcodes from: https://qrfy.com
"""
import cv2
import RPi.GPIO as GPIO 
from pyzbar.pyzbar import decode

# Variable Declaration
# Object to access the camera sensor and capture video frames
GPIO.setwarnings(False)
cap = cv2.VideoCapture(1) # The zero is for the default camera
frameNumber = 0 # Counter to support the task of saving a frame
qrDetector = cv2.QRCodeDetector() #QR-Code detector object
led1=2
led2=3


GPIO.setmode(GPIO.BCM)
GPIO.setup(led1,GPIO.OUT)
GPIO.setup(led2,GPIO.OUT)

GPIO.output(led1, GPIO.LOW)
GPIO.output(led2, GPIO.LOW)

# Validate if camera sensor opened as expected
if not cap.isOpened():
    print("Error: Could not open the camera.")
    exit()

# Loop to continuosly to capture frames from the camera
while True:
    # Read a frame from the camera
    ret,frame = cap.read()
    # ret is true when frame is read correctly
    if not ret:
        print("Error: Could not read a frame")
        break
    # Avoid incorrect frames that can crash video streaming
    try:
	# Obtain the QRCode from the current frame
        data= decode(frame)
        # Display data from QR-Code
        if data:
            value=data[0].data.decode("utf-8")
            print("Encoded Data Result: ",value)
            if value == '1':
                GPIO.output(led1, GPIO.HIGH)
                GPIO.output(led2, GPIO.LOW)
            elif value =='2':
                GPIO.output(led2, GPIO.HIGH)
                GPIO.output(led1, GPIO.LOW)
            
        else:
            GPIO.output(led1, GPIO.HIGH)
            GPIO.output(led2, GPIO.HIGH)
            print("Waiting for qr code")
            
    except Exception as e:
        print("An error ocurred during QR code detection: ", str(e))
    
    # Display the frame in a window
    cv2.imshow("Camera View", frame)
    # Check for keypress and save the frame as an image if required
    key = cv2.waitKey(1)
    if key == ord('s'):
        frameNumber +=1
        fileName = f"/home/gil/Python101/sensors/computerVision/camCalibration/calib1_{frameNumber}.png"
        cv2.imwrite(fileName,frame)
        print(f"Saved {fileName}") 
    # Terminate camera video streaming 
    if key & 0xFF == ord('q'):
        break
# Release the camera sensor and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
