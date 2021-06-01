import numpy as np
import cv2


class Parameters():
    n_epoch = 1000
    l_rate = 0.001
    weight_decay = 1e-5
    save_path = "Lane/models/"
    model_path = "Lane/models/"
    batch_size = 12
    x_size = 512
    y_size = 256
    resize_ratio = 8
    grid_x = x_size//resize_ratio  # 64
    grid_y = y_size//resize_ratio  # 32

    feature_size = 4
    regression_size = 110
    mode = 1
    threshold_point = 0.65  # 0.88 #0.93 #0.95 #0.93
    threshold_instance = 0.15

    # loss function parameter
    K1 = 1.0
    K2 = 2.0
    constant_offset = 0.2
    constant_exist = 2.5  # 2
    constant_nonexist = 1.0
    constant_angle = 1.0
    constant_similarity = 1.0
    constant_attention = 0.01
    constant_alpha = 0.5  # in SGPN paper, they increase this factor by 2 every 5 epochs
    constant_beta = 0.5
    constant_l = 1.0
    constant_lane_loss = 1.0  # 10  ######################################
    constant_instance_loss = 1.0

    # data loader parameter
    flip_ratio = 0.6
    translation_ratio = 0.6
    rotate_ratio = 0.6
    noise_ratio = 0.6
    intensity_ratio = 0.6
    shadow_ratio = 0.6

    # train_root_url="/home/phuoc/Desktop/project AI/cam_1/"
    # test_root_url="/home/phuoc/Desktop/project AI/cam_1/"

    # test parameter
    color = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255),
             (255, 255, 255), (100, 255, 0), (100, 0, 255), (255, 100, 0), (0, 100, 255), (255, 0, 100), (0, 255, 100)]
    grid_location = np.zeros((grid_y, grid_x, 2))
    for y in range(grid_y):
        for x in range(grid_x):
            grid_location[y][x][0] = x
            grid_location[y][x][1] = y

    num_iter = 45
    threshold_RANSAC = 0.1
    ratio_inliers = 0.1

    # expand

    point_in_lane = 0
    source_points = np.float32([
        [0, y_size],
        [0, (5/9)*y_size],
        [x_size, (5/9)*y_size],
        [x_size, y_size]
    ])

    destination_points = np.float32([
        [0 * x_size, y_size],
        [0 * x_size, 0],
        [x_size - (0 * x), 0],
        [x_size - (0 * x), y_size]
    ])

    perspective_transform = cv2.getPerspectiveTransform(
        source_points, destination_points)
    inverse_perspective_transform = cv2.getPerspectiveTransform(
        destination_points, source_points)
