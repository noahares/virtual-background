import cv2
import requests
import numpy
import os
import pyfakewebcam

def get_mask(frame, bodypix_url='http://localhost:9000'):
    _, data = cv2.imencode(".jpg", frame)
    r = requests.post(
            url=bodypix_url,
            data=data.tobytes(),
            headers={'Content-Type': 'application/octet-stream'})

    mask = numpy.frombuffer(r.content, dtype=numpy.uint8)
    mask = mask.reshape(frame.shape[0], frame.shape[1])
    return mask

def post_process_mask(mask):
    mask = cv2.dilate(mask, numpy.ones((10,10), numpy.uint8), iterations=1)
#     mask = cv2.erode(mask, numpy.ones((10,10), numpy.uint8) , iterations=1)
    mask = cv2.blur(mask.astype(float), (30,30))
    return mask

def get_frame(cap, background_scaled):
    _, frame = cap.read()
    mask = None
    while mask is None:
        try:
            mask = get_mask(frame)
        except requests.RequestException:
            print("mask request failed, retrying")

    mask = post_process_mask(mask)
    inv_mask = 1-mask
    for c in range(frame.shape[2]):
        frame[:,:,c] = frame[:,:,c]*mask + replacement_bg[:,:,c]*inv_mask
    return frame

replacement_bg_raw = cv2.imread("backgrounds/iss.jpg")
width, height = 640, 480
replacement_bg = cv2.resize(replacement_bg_raw, (width, height))

cap = cv2.VideoCapture('/dev/video0')

fake = pyfakewebcam.FakeWebcam('/dev/video20', width, height)

while True:
    frame = get_frame(cap, replacement_bg)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    fake.schedule_frame(frame)
