import torch
import torch.nn as nn
from Lane.util_hourglass import *


class lane_network(nn.Module):
    def __init__(self):
        super(lane_network, self).__init__()

        self.resizing = resize_layer(3, 128)

        self.layer1 = hourglass_block(128, 128)
        # self.layer2 = hourglass_block(128, 128)
        # self.layer3 = hourglass_block(128, 128)
        # self.layer4 = hourglass_block(128, 128)

    def forward(self, inputs):

        out = self.resizing(inputs)
        result1, out, feature1 = self.layer1(out)
        # result2, out, feature2 = self.layer2(out)
        # result3, out, feature3 = self.layer3(out)
        # result4, out, feature4 = self.layer4(out)

        # return [result1, result2, result3, result4], [feature1, feature2, feature3, feature4]
        # return [result1,result2], [feature1,feature2]
        return [result1], [feature1]
