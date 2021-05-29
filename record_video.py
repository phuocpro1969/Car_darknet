import cv2
import base64
import numpy as np
import socketio
import eventlet
import eventlet.wsgi
from PIL import Image
from flask import Flask
from io import BytesIO


class record():
    
    def __init__(self, width, height):

        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter('train_1.avi', self.fourcc, 30, (width,height))
    
    def write(self, image):
        self.out.write(image)
    
    def release(self):
        self.out.release()




    
#initialize our server
sio = socketio.Server()
#our flask (web) app
app = Flask(__name__)
#registering event handler for the server
class_colors = []
re = record(320,180)

@sio.on('telemetry')
def telemetry(sid, data):
    if data:

        steering_angle = float(data["steering_angle"])
        speed = float(data["speed"])
        image = Image.open(BytesIO(base64.b64decode(data["image"])))
        image = np.asarray(image)
        
        
        sendBack_angle = 0
        sendBack_Speed = 70
        try:
        #     #------------------------------------------  Work space  ----------------------------------------------#

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, (320,180))
            re.write(image)

            
        #     #------------------------------------------------------------------------------------------------------#
            # print('{} : {}'.format(sendBack_angle, sendBack_Speed))
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
    
 
    
    #-----------------------------------  Setup  ------------------------------------------#
    print('I am loading model right now, pls wait a minute')
   

    print('Hey Your computer has GPU, right?')

    
    #--------------------------------------------------------------------------------------#
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)
    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)