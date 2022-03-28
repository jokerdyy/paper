import time, math
from servo import Servos
from machine import I2C, Pin

i2c = I2C(sda=Pin('P5'), scl=Pin('P4'))
servo = Servos(i2c, address=0x40, freq=50, min_us=650, max_us=2800, degrees=180)

hand_speed=13

servo0_reset_angle=90
servo1_reset_angle=40
servo2_reset_angle=5
servo3_reset_angle=35

servo0_goal_angle=80
servo1_goal_angle=80
servo2_goal_angle=90
servo3_goal_angle=servo3_reset_angle

servo0_goal2_angle=65
servo1_goal2_angle=70
servo2_goal2_angle=70
servo3_goal2_angle=servo3_reset_angle

servo0_forward1_angle=42
servo1_forward1_angle=78
servo2_forward1_angle=72
servo3_forward1_angle=15

servo0_forward_angle=35
servo1_forward_angle=90
servo2_forward_angle=65
servo3_forward_angle=servo3_forward1_angle

servo0_forward2_angle=14
servo1_forward2_angle=138
servo2_forward2_angle=90
servo3_forward2_angle=servo3_forward1_angle

servo0_home_angle=60
servo1_home_angle=70
servo2_home_angle=10
servo3_home_angle=servo3_reset_angle

servo0_home1_angle=50
servo1_home1_angle=80
servo2_home1_angle=4
servo3_home1_angle=servo3_reset_angle



class Hand:
    def __init__(self, port, degree, goal):

        self.port = port
        self.degree = degree
        self.goal = goal


    def show_input(self):
        print("port,degree,goal,self.speed", self.port,self.degree,self.goal)

    pass
    ##复位为输入角度
    def reset(self):
        servo.position(self.port, self.degree)
    ##角度误差复位
    def action(self):
        pass
        if self.degree==self.goal:
            return(0)
        elif self.degree<self.goal:
            self.degree+=1
        elif self.degree>self.goal:
            self.degree-=1
        servo.position(self.port, self.degree)

servo0=Hand(0,servo0_goal_angle,servo0_reset_angle)
servo1=Hand(1,servo1_goal_angle,servo1_reset_angle)
servo2=Hand(2,servo2_goal_angle,servo2_reset_angle)
servo3=Hand(3,servo3_goal_angle,servo3_reset_angle)

#3（30，120）0（0,130）1（0，180）2（0,140）


def hand_two_reset():
    pass
    servo0.goal=servo0_reset_angle
    servo1.goal=servo1_reset_angle
    servo2.goal=servo2_reset_angle
    servo3.goal=servo3_reset_angle
    while(True):
        pass
        ser0=servo0.action()
        ser1=servo1.action()
        ser2=servo2.action()
        ser3=servo3.action()
        time.sleep(hand_speed)
        if ser0==0 and ser1==0 and ser2==0 and ser3==0:
            break


def hand_three_reset():
    pass
    servo0.goal=servo0_goal_angle
    servo1.goal=servo1_goal_angle
    servo2.goal=servo2_goal_angle
    servo3.goal=servo3_goal_angle
    while(True):
        pass
        ser0=servo0.action()
        ser1=servo1.action()
        ser2=servo2.action()
        ser3=servo3.action()
        time.sleep(hand_speed-5)
        if ser0==0 and ser1==0 and ser2==0 and ser3==0:
            break





def hand_down():
    i=1
    servo0.goal=servo0_goal_angle
    servo1.goal=servo1_goal_angle
    servo2.goal=servo2_goal_angle
    while(True):
        pass
        i=i+1
        #ser0=servo0.action()
        ser0=servo0.action()
        ser1=servo1.action()
        ser2=servo2.action()
        if ser0==0 and ser1==0 and ser2==0:
            break
        time.sleep(hand_speed-5)

def hand_down_two():
    i=1
    servo0.goal=servo0_goal2_angle
    servo1.goal=servo1_goal2_angle
    servo2.goal=servo2_goal2_angle
    while(True):
        pass
        i=i+1
        #ser0=servo0.action()
        ser0=servo0.action()
        ser1=servo1.action()
        ser2=servo2.action()
        if ser0==0 and ser1==0 and ser2==0:
            break
        time.sleep(hand_speed-5)

def hand_close():
    servo3.goal=servo3_goal_angle
    while(True):
        ser3=servo3.action()
        time.sleep(hand_speed)
        if ser3==0:
            break



def hand_forward(max_ball_high):
    i=1
    if 30<=max_ball_high<=55:
        servo0.goal=servo0_forward_angle
        servo1.goal=servo1_forward_angle
        servo2.goal=servo2_forward_angle
    elif max_ball_high>55:
        servo0.goal=servo0_forward1_angle
        servo1.goal=servo1_forward1_angle
        servo2.goal=servo2_forward1_angle
    elif max_ball_high<30:
        servo0.goal=servo0_forward2_angle
        servo1.goal=servo1_forward2_angle
        servo2.goal=servo2_forward2_angle
    while(True):
        if max_ball_high<30:
            i=i+1
            if i<10:
                ser1=servo1.action()
                time.sleep(hand_speed)
            else:
                ser0=servo0.action()
                ser1=servo1.action()
                ser2=servo2.action()
                if ser0==0 and ser1==0 and ser2==0:
                    break
                time.sleep(hand_speed)
        else:
            ser0=servo0.action()
            ser1=servo1.action()
            ser2=servo2.action()
            if ser0==0 and ser1==0 and ser2==0:
                break
            time.sleep(hand_speed)

def hand_up():
    servo0.goal=servo0_reset_angle
    servo1.goal=servo1_reset_angle
    servo2.goal=servo2_reset_angle
    servo3.goal=servo3_forward_angle
    while(True):
        ser3=servo3.action()
        time.sleep(4)
        if ser3==0:
            break
    time.sleep(200)
    i=1
    while(True):
        pass
        i=i+1
        if i<=10:
            ser2=servo2.action()
        else:
            ser0=servo0.action()
            ser1=servo1.action()
            ser2=servo2.action()
            if ser0==0 and ser1==0 and ser2==0:
                break
        time.sleep(hand_speed-5)
def hand_shot_ready():
    pass
    servo0.goal=servo0_home_angle
    servo1.goal=servo1_home_angle
    servo2.goal=servo2_home_angle
    while(True):
        pass
        ser0=servo0.action()
        ser1=servo1.action()
        ser2=servo2.action()
        time.sleep(hand_speed-5)
        if ser0==0 and ser1==0 and ser2==0:
            break

def hand_shot_ready_more():
    pass
    servo0.goal=servo0_home1_angle
    servo1.goal=servo1_home1_angle
    servo2.goal=servo2_home1_angle
    while(True):
        pass
        ser0=servo0.action()
        ser1=servo1.action()
        ser2=servo2.action()
        time.sleep(hand_speed-5)
        if ser0==0 and ser1==0 and ser2==0:
            break

def hand_shot():
    pass
    servo3.goal=servo3_home_angle

    while(True):
        ser3=servo3.action()
        time.sleep(hand_speed-5)
        if ser3==0:
            break

    pass

def first_reset():
    servo0.reset()
    servo1.reset()
    servo2.reset()
    servo3.reset()
