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




    def update(self, SetStatusObjs, StatusLines, StatusBoxes, objs_disappear):
        self.StatusObjs = SetStatusObjs
        self.StatusLines = StatusLines
        self.StatusBoxes = StatusBoxes
        self.objs_disappear = objs_disappear

        

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
            self.time -= 1

        else:
            if 'i10' in self.objs_disappear:
                self.handle_i10()
                self.flag = 'i10'
                self.tweakAngle = 25
                # if self.StatusLines[0] == 3:
                #     self.speed = -5
                #     self.time = 70
                # else:
                self.speed = 30
                self.time = 30
                #35
            
            if 'i12' in self.objs_disappear:
                self.handle_i12()
                self.flag = 'i12'
                self.tweakAngle = -25
                # if self.StatusLines[0] == 3:
                #     self.speed = -3
                # else:
                self.speed = -2
                self.time = 32
                #35
            if 'i13' in self.objs_disappear:
                self.handle_i13()
                self.flag = 'i13' 
                if 'i5' in self.StatusObjs[-1]:
                    index = list(self.StatusObjs[-1]).index('i5')
                    bbox_i5 = self.StatusBoxes[-1][index]
                    left, top, right, bottom = darknet.bbox2points(bbox_i5)
                    x_center = int(( left + right ) / 2 / 224 * 512)
                    if x_center > 200 and x_center < 412:
                        self.tweakAngle = util.errorAngle((x_center + 35, 128))
                        self.speed = 15
                        self.time = 15
                # else:
                #     self.tweakAngle = 0
                #     self.speed = 50
                #     self.time = 15



            if 'p19' in self.objs_disappear:
                self.handle_p19()
                self.flag = 'p19'
                if 'i5' in self.StatusObjs[-1]:
                    index = list(self.StatusObjs[-1]).index('i5')
                    bbox_i5 = self.StatusBoxes[-1][index]
                    left, top, right, bottom = darknet.bbox2points(bbox_i5)
                    x_center = int(( left + right ) / 2 / 224 * 512)
                    if x_center > 150 and x_center < 462:
                        self.tweakAngle = util.errorAngle((x_center + 35, 128))
                        self.speed = 30
                        self.time = 17

                elif all(np.array(self.StatusLines[-3:]) < 1):
                    self.tweakAngle = -25
                    self.speed = -2
                    self.time = 30
                
                else:
                    self.tweakAngle = -25
                    self.speed = 25
                    self.time = 15

            if 'p23' in self.objs_disappear:
                self.handle_p23()
                self.flag = 'p23'
                if 'i5' in self.StatusObjs[-1]:
                    index = list(self.StatusObjs[-1]).index('i5')
                    bbox_i5 = self.StatusBoxes[-1][index]
                    print(bbox_i5)
                    left, top, right, bottom = darknet.bbox2points(bbox_i5)
                    x_center = int(( left + right ) / 2 / 224 * 512)
                    if x_center > 150 and x_center < 462:
                        self.tweakAngle = util.errorAngle((x_center + 65, 128))
                        self.speed = 10
                        self.time = 30

                elif all(np.array(self.StatusLines[-3:]) < 1):
                    self.tweakAngle = 25
                    self.speed = -2
                    self.time = 30

    
    def handle_i10(self):
        print("handle_i10")
        self.flag = False
        self.tweakAngle = None
        self.speed = None
    
    def handle_i12(self):
        print("handle_i12")
        self.flag = False
        self.tweakAngle = None
        self.speed = None

    def handle_i13(self):
        print("handle_i13")
        self.flag = False
        self.tweakAngle = None
        self.speed = None

    def handle_p19(self):
        print("handle_p12")
        self.flag = False
        self.tweakAngle = None
        self.speed = None

    def handle_p23(self):
        print("handle_p23")
        self.flag = False
        self.tweakAngle = None
        self.speed = None        

