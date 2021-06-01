"""
        * depth_image: set takeDepth = True,  depth image will return when 'send_control' sent)
        + sendBack_angle [-25, 25]  
        + sendBack_Speed [-150, 150] 
"""
import base64
import numpy as np
import socketio
import eventlet
import eventlet.wsgi
import cv2
from PIL import Image
from flask import Flask
from io import BytesIO

# My import 
from Lane.net import Net
from Lane.parameters import Parameters
from Lane import util
import darknet
from rules import Rule
import copy

import torch
import time

# My setup

net = Net()
p = Parameters()
warning = []
SetStatusObjs = []
StatusLines = []
StatusBoxes = []

#Global variable
MAX_SPEED = 30
MAX_ANGLE = 25
#Tốc độ thời điểm ban đầu
speed_limit = MAX_SPEED
MIN_SPEED = 10

#init our model and image array as empty


#initialize our server
sio = socketio.Server()
#our flask (web) app
app = Flask(__name__)
#registering event handler for the server
flag_stop = False

@sio.on('telemetry')
def telemetry(sid, data):
    if data:
        global SetStatusObjs
        global StatusLines
        global StatusBoxes
        global flag_stop
        steering_angle = float(data["steering_angle"])
        speed = float(data["speed"])
        image = Image.open(BytesIO(base64.b64decode(data["image"])))
        image = np.asarray(image)
        
        
        sendBack_angle = 0
        sendBack_Speed = 70
        try:
        #   #------------------------------------------  Work space  ----------------------------------------------#
            if flag_stop:
                if speed <= 2:
                    send_control(0,0)
                else:
                    send_control(0,-150)
                print("STOP")
                # if speed == 0:
                    
            else:
                prevTime = time.time()
                ###Traffic
                image_resized = cv2.resize(image, (width, height),
                                        interpolation=cv2.INTER_LINEAR)
                darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
                
                detections = np.array(darknet.detect_image(yolov4, class_names, darknet_image, thresh=thresh), dtype=object)
                
                
                ###Lane 
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = cv2.resize(image,(512,256))
            
                x, y = net.predict(image)
                # fits = np.array([np.polyfit(_y, _x, 1) if len(_x) < 5  else  np.polyfit(_y, _x, 2) for _x, _y in zip(x, y)])
                fits = np.array([np.polyfit(_y, _x, 1) for _x, _y in zip(x, y)])
                
                fits = util.adjust_fits(fits)
                
                StatusLines.append(len(fits))

                if len(StatusLines) > 8:
                    StatusLines = StatusLines[-8:]
                

                mask = net.get_mask_lane(fits)
                curTime = time.time()
                # image_lane = net.get_image_points()
                sendBack_angle = util.get_steer_angle(fits)
                
                

                labels = confidences = bboxes = np.array([])

                if len(detections) != 0:
                    sendBack_Speed = 0
                    labels, confidences, bboxes =  detections[:,0], detections[:,1], detections[:,2]
                    if 'car' in labels:
                        bbox = bboxes[list(labels).index('car')]
                        left, top, right, bottom = darknet.bbox2points(bbox)
                        center = [int((left + right) // 2 / 224 * image.shape[1]), int(((top + bottom) // 2 + 30) / 224 * image.shape[0])]
                        if center[0] > 511:
                            center[0] = 511
                        if center[1] > 255:
                            center[1] = 255

                        #### continue here
                        index = [i for i in range(len(net.colours)) if all(net.colours[i] == mask[center[1], center[0]])]

                        if index == [1]:
                            fits = fits[:-1]
                            sendBack_angle = util.get_steer_angle(fits)
                        else:
                            pass
                    if 'i10' in labels:
                        sendBack_Speed = 10

                    SetStatusObjs.append(set(labels))
                    StatusBoxes.append(bboxes)
                    
                else:
                    SetStatusObjs.append(set())
                    StatusBoxes.append([])
                    sendBack_Speed = util.calcul_speed(sendBack_angle)
                if len(SetStatusObjs) > 6:
                    SetStatusObjs = SetStatusObjs[-6:]
                    StatusBoxes =  StatusBoxes[-6:]
                    # print(SetStatusObjs)

                t = np.array([ 1 if 'stop' in sobjs else 0 for sobjs in SetStatusObjs ])
                if len(np.where(t == 1)[0]) > 3:
                    flag_stop = True


                #get object disappear
                objs_disappear = []
                # print(SetStatusObjs)
                if len(SetStatusObjs) >= 5:
                    temp = [obj.copy() for obj in SetStatusObjs]
                    cleared_StatusObjs = util.clear_StatusObjs(temp)
                    first_labels = cleared_StatusObjs[0]
                    first_sub = first_labels - cleared_StatusObjs[1]
                    # print(first_sub)
                    if len(first_sub) == 0:
                        pass
                    elif all([ first_sub == (first_labels - set_detection) for set_detection in cleared_StatusObjs[2:]]):
                        objs_disappear = first_sub
                        print(objs_disappear)    


                # include SetStatusObjs, StatusLines, objs_disappear

                ru.update(SetStatusObjs, StatusLines, StatusBoxes, objs_disappear)
                ru.handle()
                ruAngle, ruSpeed = ru.get_result()
                
                if ruAngle != None:
                    sendBack_angle = ruAngle
                    sendBack_Speed = ruSpeed


                sec = curTime - prevTime
                fps = 1/(sec)
                s = "FPS : "+ str(fps)
                # print(s)
                image_lane = net.get_image_lane()
                image_lane = darknet.draw_boxes(detections, image_lane, class_colors)
                # cv2.putText(image_lane, s, (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
                cv2.imshow("image", image_lane)
                cv2.waitKey(1)

                
                #------------------------------------------------------------------------------------------------------#
                # print('{} : {}'.format(sendBack_angle, sendBack_Speed))
                if speed > MAX_SPEED:
                    sendBack_Speed = 5
                if speed < 10:
                    sendBack_Speed = 100
                send_control(sendBack_angle, sendBack_Speed)
        except Exception as e:
            print(e)
    else:
        sio.emit('manual', data={}, skip_sid=True)

@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)
    send_control(0, 0)


def send_control(steering_angle, throttle):
    sio.emit(
        "steer",
        data={
            'steering_angle': steering_angle.__str__(),
            'throttle': throttle.__str__(),
        },
        skip_sid=True)


if __name__ == '__main__':
    
    config_file = "./cfg/tiny-traffic-sign.cfg"
    weights = "./models/tiny-traffic-sign_best.weights"
    data_file = "./cfg/tiny-traffic-sign.data"
    
    #-----------------------------------  Setup  ------------------------------------------#
    print('I am loading model right now, pls wait a minute')
    net.load_model(34,"tensor(0.7828)")

    yolov4, class_names, class_colors = darknet.load_network(config_file, data_file, weights, 1)
    width = darknet.network_width(yolov4)
    height = darknet.network_height(yolov4)
    darknet_image =  darknet.make_image(width, height, 3)
    thresh = 0.95 # 0.88
    ru = Rule()

    print('Hey Your computer has GPU, right?')

    
    #--------------------------------------------------------------------------------------#
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)
    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)
