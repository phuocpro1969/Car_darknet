from Lane.net import Net
import cv2
import time
from Lane.util import adjust_fits, get_steer_angle
import numpy as np
net = Net()
net.load_model(7,"tensor(0.5741)")

cap = cv2.VideoCapture("out.avi")

while True:

    ret, frame = cap.read()
    prevTime = time.time()

    x, y = net.predict(frame)
    fits = np.array([np.polyfit(_y, _x, 2) for _x, _y in zip(x, y)])
    fits = adjust_fits(fits)
    image_lane = net.get_image_lane(fits)
    steer_angle = get_steer_angle(fits)

    curTime = time.time()
    sec = curTime - prevTime
    fps = 1/(sec)
    s = "FPS : "+ str(fps)
    cv2.putText(image_lane, s, (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))

    cv2.imshow("image", image_lane)
    k = cv2.waitKey(1)
    if k == ord("q"):
        break