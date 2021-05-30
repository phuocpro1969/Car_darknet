import numpy as np
import darknet
import Lane.util as util


class Rule():
    def __init__(self, SetStatusObjs = [], StatusLines = [], StatusBoxes = [], objs_disappear = []):

        self.StatusObjs = SetStatusObjs
        self.StatusLines = StatusLines
        self.objs_disappear = objs_disappear
        self.StatusBoxes = StatusBoxes
        self.tweakAngle = None
        self.speed = None
        self.flag = False
        self.time = 0
        self.prev_flag = None


    def update_run(self, tweakAngle, speed, flag, time, prev_flag):
        self.tweakAngle = tweakAngle
        self.speed = speed
        self.flag = flag
        self.time = time
        self.prev_flag = prev_flag


    def update(self, SetStatusObjs, StatusLines, StatusBoxes, objs_disappear):
        self.StatusObjs = SetStatusObjs
        self.StatusLines = StatusLines
        self.StatusBoxes = StatusBoxes
        self.objs_disappear = objs_disappear

    def clear_handle(self, name):
        print(name)
        self.flag = False
        self.tweakAngle = None
        self.speed = None 
        self.prev_flag = None      

    def get_result(self):
        return self.tweakAngle, self.speed

    def handle(self):    
        if self.flag is not False:
            print(self.StatusObjs, self.StatusLines, self.objs_disappear)
            if (all(np.array(self.StatusLines[-3:]) >= 2) and self.time < 10) or self.time <= 0:
                print("stoped flag handle")
                self.flag = False
                self.tweakAngle = None
                self.speed = None

            if self.flag == 'i12':
                if 'i5' in self.StatusObjs[-1]:
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    index = list(self.StatusObjs[-1]).index('i5')
                    bbox_i5 = self.StatusBoxes[-1][index]
                    left, top, right, bottom = darknet.bbox2points(bbox_i5)
                    x_center = int(( left + right ) / 2 / 224 * 512)
                    y_center = int(( top + bottom ) / 2 / 224 * 256)
                    if x_center < 256:
                        self.tweakAngle = util.errorAngle((x_center + 120, y_center))
                        self.speed = 30
                        self.time = 20

            if self.prev_flag == 'p19':
                if 'p19' not in self.objs_disappear and self.StatusLines[7]<3: # check can't go a head
                    self.tweakAngle = -25
                    self.speed = 30
                    self.time = 20
                    self.prev_flag = None
                    self.update_run(flag=self.flag, tweakAngle=-25, speed=30, time=20, prev_flag=None)
            
            self.time -= 1
            if self.prev_flag and self.time == 0:
                self.prev_flag = None

        else:
            if 'i10' in self.objs_disappear:
                self.clear_handle("i10")
                self.update_run(flag='i10', tweakAngle=25, speed=30, time=28, prev_flag=None)
            
            if 'i12' in self.objs_disappear:
                self.clear_handle("i12")
                self.update_run(flag='i12', tweakAngle=-25, speed=-2, time=32, prev_flag=None)

            if 'i13' in self.objs_disappear:
                self.clear_handle("i13")
                self.flag = 'i13' 
                if 'i5' in self.StatusObjs[-1]:
                    index = list(self.StatusObjs[-1]).index('i5')
                    bbox_i5 = self.StatusBoxes[-1][index]
                    left, top, right, bottom = darknet.bbox2points(bbox_i5)
                    x_center = int(( left + right ) / 2 / 224 * 512)
                    if x_center > 200 and x_center < 412:
                        angle= util.errorAngle((x_center + 38, 128))
                        self.update_run(flag='i13', tweakAngle=angle, speed=15, time=20, prev_flag=None)
                # else:
                #     self.tweakAngle = 0
                #     self.speed = 50
                #     self.time = 15

            if 'p19' in self.objs_disappear:
                self.clear_handle("p19")
                if 'i5' in self.StatusObjs[-1]:
                    # di vao noi co bien i5
                    index = list(self.StatusObjs[-1]).index('i5')
                    bbox_i5 = self.StatusBoxes[-1][index]
                    left, top, right, bottom = darknet.bbox2points(bbox_i5)
                    x_center = int(( left + right ) / 2 / 224 * 512)
                    if x_center > 150 and x_center < 462:
                        angle = util.errorAngle((x_center + 45, 128))
                        self.update_run(flag='i13', tweakAngle=angle, speed=30, time=17, prev_flag=None)

                elif all(np.array(self.StatusLines[-3:]) < 1):
                    # left
                    self.update_run(flag='i13', tweakAngle=-25, speed=-2, time=30, prev_flag=None)
                
                else:
                    # right
                    self.update_run(flag='i13', tweakAngle=0, speed=30, time=17, prev_flag='p19')

            if 'p23' in self.objs_disappear:
                self.clear_handle("p23")
                if 'i5' in self.StatusObjs[-1]:
                    index = list(self.StatusObjs[-1]).index('i5')
                    bbox_i5 = self.StatusBoxes[-1][index]
                    print(bbox_i5)
                    left, top, right, bottom = darknet.bbox2points(bbox_i5)
                    x_center = int(( left + right ) / 2 / 224 * 512)
                    if x_center > 150 and x_center < 462:
                        self.update_run(flag='p23', tweakAngle=angle, speed=10, time=30, prev_flag=None)

                elif all(np.array(self.StatusLines[-3:]) < 1):
                    self.update_run(flag='p23', tweakAngle=25, speed=-2, time=30, prev_flag=None) 
