import cv2
import darknet
import time
import numpy as np

from Lane.net import Net
from Lane.parameters import Parameters
from Lane import util


vcap = cv2.VideoCapture("test.avi")
config_file = "./cfg/tiny-traffic-sign.cfg"
weights = "./models/tiny-traffic-sign_best.weights"
data_file = "./cfg/tiny-traffic-sign.data"
yolov4, class_names, class_colors = darknet.load_network(config_file, data_file, weights, 1)
width = darknet.network_width(yolov4)
height = darknet.network_height(yolov4)
darknet_image =  darknet.make_image(width, height, 3)
thresh = 0.5
net = Net()
p = Parameters()
net.load_model(9,"tensor(0.5805)")


while(True):

    ret, frame = vcap.read()

    if not ret:
        break
    image = cv2.resize(frame,(512,256))

    prev_time = time.time()
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_rgb, (width, height),
                            interpolation=cv2.INTER_LINEAR)
    darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
    detections = darknet.detect_image(yolov4, class_names, darknet_image, thresh=thresh)
    detections = np.array(detections, dtype=object)
    

    x, y = net.predict(image)
    fits = np.array([np.polyfit(_y, _x, 1) for _x, _y in zip(x, y)])
    fits = util.adjust_fits(fits)

    mask = net.get_mask_lane(fits)
    print(mask.shape)
    # image_lane = net.get_image_lane()
    
    if len(detections) == 0: # dont have any object are detected in image
        pass

    else:
        labels = detections[:,0]
        confidences = detections[:,1]
        bboxes = detections[:,2]
        
        if 'car' in labels:
            left, top, right, bottom = darknet.bbox2points(bboxes[list(labels).index('car')])
            car_center = [(left + right) // 2 , (top + bottom) // 2]
            
            # which do lane car inside?

            # in car in right lane : drive car to left lane and opposite 

        if 'i10' in labels: # go straight ahead
            warn.append('i10')
        
        if 'i12' in labels: # turn left
            warn.append('i12')
        
        if 'i13' in labels: # turn right
            warn.append('i13')

        if 'p19' in labels: # ban turn right
            warn.append('p19')
        
        if 'p23' in labels: # ban turn left
            warn.append('p23')
    # fits = np.array([np.polyfit(_y, _x, 1) if len(_x) < 5  else  np.polyfit(_y, _x, 2) for _x, _y in zip(x, y)])
    end_time = time.time()
    fps = 1/(end_time - prev_time)
    print(fps)

    mask = darknet.draw_boxes(detections, mask, class_colors)
    cv2.imshow("image", mask)
    cv2.waitKey(1)