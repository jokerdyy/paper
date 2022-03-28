# 舵机控制
#   1. 连接舵机到任何PWM输出。
#   2. 将3.7v电池（或5V电源）连接到VIN和GND。
#   3. 将pca9685.py和servo.py复制到OpenMV并重置。
#   4. 在IDE中连接并运行此脚本。

import sensor, image, time, math

from servo import Servos
from machine import I2C, Pin

red_threshold = (2, 72, -38, -14, 21, 50) #(47, 100, -22, 67, 41, 77)

sensor.reset()  # 初始化摄像头
sensor.set_pixformat(sensor.RGB565)  # 格式为 RGB565.
sensor.set_framesize(sensor.QQVGA)  # 使用 QQVGA 速度快一些
sensor.skip_frames(time=2000)  # 跳过2000s，使新设置生效,并自动调节白平衡
sensor.skip_frames(10)  # Let new settings take affect.

sensor.set_auto_gain(False)  # 关闭自动自动增益。默认开启的，在颜色识别中，一定要关闭白平衡。
sensor.set_auto_whitebal(False)
# 关闭白平衡。白平衡是默认开启的，在颜色识别中，一定要关闭白平衡。
clock = time.clock()  # 追踪帧率

i2c = I2C(sda=Pin('P5'), scl=Pin('P4'))
servo = Servos(i2c, address=0x40, freq=50, min_us=650, max_us=2800, degrees=180)

K = 5000  # the value should be measured得到mm
x_chassis = 0
y_chassis = 0
x_camera = 0
l_camera = 0
i = 0
arm_angle_goal = 0
elbow_angle_goal = 0
chassised_angle = 0
chassised_angle_goal = 0
chassis_angle_goal = 0
arm_ball = 0
chassis_ball = 0
chassis_high = 0
chassis_angle = 0  # 底盘舵机角度
arm_angle = 0  # 臂舵机角度
elbow_angle = 0  # 肘舵机角度
hand_angle = 0  # 手爪舵机角度

max_chassis_angle = 180  # 底盘舵机复位角度
min_chassis_angle = 0  # 底盘舵机有效角度
max_arm_angle = 90  # 臂舵机复位角度
min_arm_angle = 0  # 臂舵机有效角度
max_elbow_angle = 180  # 肘舵机复位角度
min_elbow_angle = 0  # 肘舵机有效角度
max_hand_angle = 60  # 手爪舵复位机角度
min_hand_angle = 10  # 手爪舵机有效角度

x_camera = 0  # 小球对于摄像头x坐标
y_camera = 0  # 小球对于摄像头y坐标
x_chassis = 0  # 小球对于底盘x坐标
y_chassis = 0  # 小球对于底盘y坐标
i = 0

arm_angle_camera = 0  # 手臂和水平线角度
arm_ball = 0  # 臂舵机到球距离
elbow_angle_camera = 0  # 肘舵机于竖线的角度

chassis_high = 100  # 底座高度mm 90-20=70
arm_long = 210  # 手臂长度
elbow_hand_long = 190  # 手爪到肘长
chassis_ball = 0  # 底座到球距离

while (True):
    servo.position(1, 50)
    time.sleep(3000)
    servo.position(0, 60)
    time.sleep(300)

    servo.position(2, 0)
    time.sleep(300)

    print('进入')
    while (i < 11):
        i = i + 1
        clock.tick()  # Track elapsed milliseconds between snapshots().
        img = sensor.snapshot()  # 从感光芯片获得一张图像

        blobs = img.find_blobs([red_threshold])
        if blobs:
            # 如果找到了目标颜色
            for b in blobs:
                # 迭代找到的目标颜色区域
                # Draw a rect around the blob.
                img.draw_rectangle(b[0:4])  # rect
                # 用矩形标记出目标颜色区域
                img.draw_cross(b[5], b[6])  # cx, cy
                # 在目标颜色区域的中心画十字形标记
        Lm = (b[2]+b[3])/2
        length = K / Lm  # 球到摄像头距离
        x_camera = x_camera + b[5]  # 为了求x点在感兴趣区域的坐标x平均
        l_camera = l_camera + length  # 距离累加10次
        print('正在获取小球对于球的坐标，距离，x坐标：', length, int(length), b[5])
        print("jili")
        print(length)
        # print(b[5])
        time.sleep(30)
    x_camera = x_camera / 10
    l_camera = l_camera / 10 - 20
    x_chassis = math.sin((x_camera - 80) * 115 / 160*3.14/180) * l_camera
    #x_chassis = math.fabs(x_chassis)
    y_chassis = math.cos((x_camera - 80) * 115 / 160*3.14/180) * l_camera
    # 115是整个视野角度，平均到x方向每个像素就是115/160左边为负，右边为正，再乘以距离就是真实的偏移距离

    print('得到数据，距离平均值mm，x坐标平均值，x绝对坐标，y绝对坐标，角度')
    time.sleep(30)
    print(l_camera)
    print(x_camera)
    print(x_chassis)
    print(y_chassis)
    print((x_camera -80)* 115 / 160*3.14/180)
    # break

    # 进入抓球状态
    chassised_angle = math.atan(x_chassis / y_chassis)  # 得到相对弧度
    chassised_angle = chassised_angle * 180 / 3.14  # 转换成角度
    chassised_angle_goal = 90 - chassised_angle # 0.34=50/17  转换成舵机绝对角度
    chassised_angle_goal = chassised_angle_goal * 2/3
    print('底盘绝对角度是：')
    print(chassised_angle)

    # arm_angle_goal和elbow_angle_goal是目标角度
    chassis_ball = math.sqrt(x_chassis ** 2 + y_chassis ** 2)
    print('摄像头到球:')
    print(chassis_ball)
    arm_angle = math.atan(chassis_high / chassis_ball)  * 180 / math.pi # 角度:底座——球 & ——水平线
    arm_ball = math.sqrt(chassis_ball * chassis_ball + chassis_high * chassis_high)  # 臂舵机到球距离
    # 手臂和水平线角度余弦定理c*c = a*a + b*b - 2*a*b*cosC求反余弦减去臂舵机到球距离
    print('球到底座距离:')
    print(arm_ball)
    print('底下三角形角度:')
    print(arm_angle)
    arm_angle_goal = math.acos((arm_ball * arm_ball + arm_long * arm_long - elbow_hand_long * elbow_hand_long) / (2 * arm_ball * arm_long))
    arm_angle_goal = arm_angle_goal * 180 / math.pi  # 手臂和水平线角度45/
    arm_angle_goal = arm_angle_goal - arm_angle
    elbow_angle_goal = math.acos((elbow_hand_long * elbow_hand_long + arm_long * arm_long - arm_ball * arm_ball) / (2 * elbow_hand_long * arm_long)) * 180 / math.pi  # 臂肘之间的角度
    elbow_angle_goal = elbow_angle_goal - 90  # 肘舵机于竖线的角度
    arm_angle_goal = arm_angle_goal * 2/3
    elbow_angle_goal = elbow_angle_goal * 2/3 +26
    print('底座目标角度:')
    print(chassised_angle_goal)
    print('手臂目标角度:')
    print(arm_angle_goal)
    print('肘部目标角度:')
    print(elbow_angle_goal)
    pass
    servo.position(3, 0)
    time.sleep(300)
    servo.position(0, chassised_angle_goal)
    time.sleep(300)
    servo.position(1, arm_angle_goal)
    time.sleep(300)
    servo.position(2, elbow_angle_goal)
    time.sleep(3000)
    servo.position(3, 80)
    time.sleep(5000)

    servo.position(1, 30)
    time.sleep(3000)

    servo.position(0, 90)
    time.sleep(3000)
    servo.position(3, 0)
    time.sleep(300)
    break
