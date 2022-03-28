import sensor, image, time,random
import car,hand
import  math
from pid import PID

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # use RGB565.
sensor.set_framesize(sensor.QQVGA) # use QQVGA for speed.
sensor.skip_frames(60) # Let new settings take affect.
sensor.set_auto_whitebal(False) # turn this off.
clock = time.clock() # Tracks FPS.

#x_pid = PID(p=1, i=6,d=0.5, imax=100)
x_pid = PID(p=1, i=3,d=0.5, imax=100)
y_pid = PID(p=0.1, i=0.1, d=0.1, imax=40)
'''
red_threshold     = (46, 100, 40, 111, -11, 64)
#red_threshold     = (46, 77, 53, 111, -11, 64)
green_threshold   = (32, 92, -69, -34, -1, 39)
#green_threshold   = (32, 100, -77, -24, -24, 22)
blue_threshold    = (32, 77, -12, 27, -69, -25)
black_threshold   = (0, 25, -17, 15, -18, 15)
'''
red_threshold     = (43, 74, 27, 77, -8, 50)
green_threshold   = (48, 70, -78, -40, 35,60)
#green_threshold   = (32, 100, -77, -24, -24, 22)
blue_threshold    = (34, 100, -55, 3, -51, -6)
black_threshold   = (0, 25, -17, 15, -18, 15)


#ball_threshold    =  red_threshold
ball_threshold    =  blue_threshold
home_threshold    =  green_threshold
ball_high=35
home_high=95

car_speed=100
car_speed_max=car_speed
car_turn_speed=50
x_range=40
y_range=3
x_range_home=60
y_range_home=5

x_range_black=20
y_range_black=20
black_high=30

def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob[2]*blob[3] > max_size:
            max_blob=blob
            max_size = blob[2]*blob[3]
    return max_blob

def car_rotate(x_error,car_speed):
    pass
    print('旋转')
    if x_error<-5:
        car.run(car_speed,-car_speed)
    elif x_error>5:
        car.run(-car_speed,car_speed)


def car_move(y_error,y_range,car_speed):
    pass
    print('移动')
    if y_error<-y_range:
        car.run(car_speed,car_speed)
    elif y_error>y_range:
        car.run(-car_speed,-car_speed)

def car_back():
    global rand
    rand=random.randint(0,1)
    car.run(-car_speed,-car_speed)
    hand.hand_two_reset()
    if rand==0:
        car.run(car_turn_speed,-car_turn_speed)
    else:
        car.run(-car_turn_speed,car_turn_speed)
    hand.hand_down()
    #turn_time=random.randint(100,400)
    #time.sleep(turn_time)
    car.run(0,0)

def car_stop(speed):
    car.run(0,0)
    for i in range(speed):
        car.run(-i,-i)
    time.sleep(speed)
    for i in range(speed):
        car.run(i,i)
    time.sleep(speed)
    for i in range(speed-30):
        car.run(-i,-i)
    time.sleep(speed)
    for i in range(speed-30):
        car.run(i,i)
    time.sleep(speed)
    car.run(0,0)


def time_counter(ti):
    ti=ti+1
    return(ti)

def car_adjust():
    car.run(-car_speed,-car_speed)
    time.sleep(1000)
    car.run(car_speed,-car_speed)
    time.sleep(1000)
    car.run(0,0)

hand.first_reset()
time.sleep(500)
rand=1
while(True):
    k=1
    p=1
    car_speed=car_speed_max
    area=(0,0,160,120)
    ti=1
    ti_2=1
    while(True and p==1):
        clock.tick()
        img = sensor.snapshot()
        blobs = img.find_blobs([ball_threshold],roi=area)
        if blobs:
            pass
            ti=time_counter(ti)
            print('找球ti=',ti)
            if ti>600:
                car_adjust()
                p=1
                break
            max_blob = find_max(blobs)
            x1=max_blob[0]-5
            y1=max_blob[1]-5
            w1=max_blob[2]+10
            h1=max_blob[3]+10
            area=(x1,y1,w1,h1)
            x_error = max_blob[5]-80
            y_error = max_blob[3]-ball_high
            x_output=x_pid.get_pid(x_error,1)
            y_output=y_pid.get_pid(y_error,1)
            img.draw_rectangle(max_blob[0:4]) # rect
            img.draw_cross(max_blob[5], max_blob[6]) # cx, cy
            print('x_error,y_error,max_blob[3]',x_error,y_error,max_blob[3])
            if 30>max_blob[3]>15:
                x_range=30
            elif max_blob[3]>=30:
                x_range=20
            else:
                x_range=40
            pass
            if x_error<-x_range or x_error>x_range:#先调方向
                car.run(-x_output,x_output)
            else:#方向正确后if x_error<-x_range or x_error>x_range:#先调方向
                if -y_range<y_error<y_range:
                    p=2
                    car_stop(car_speed)
                    break
                else:
                    if max_blob[3]>20:
                        car_speed=70
                    elif 25>max_blob[3]>=20:
                        car_speed=60
                    elif 30>max_blob[3]>=25:
                        car_speed=55
                    elif 40>max_blob[3]>=30:
                        car_speed=48
                    elif max_blob[3]>=40:
                        car_speed=40
                    else:
                        car_speed=100
                    car_move(y_error,y_range,car_speed)




        else:
            #car.run(car_turn_speed,-car_turn_speed)
            ti_2=time_counter(ti_2)
            if ti_2>500:
                if rand==0:
                    car.run(-car_turn_speed,car_turn_speed)
                else:
                    car.run(car_turn_speed,-car_turn_speed)
                time.sleep(2000)
                car.run(car_speed,car_speed)
                time.sleep(1000)
                car.run(0,0)
                p=1
                break
            area=(0,0,160,120)
            if rand==0:
                car.run(car_turn_speed,-car_turn_speed)
            else:
                car.run(-car_turn_speed,car_turn_speed)
    car_speed=car_speed_max
    while(True and p==2):
        pass
        clock.tick()
        img = sensor.snapshot()
        blobs = img.find_blobs([ball_threshold])
        sensor.skip_frames(20)
        if blobs:
            max_blob = find_max(blobs)
            img.draw_rectangle(max_blob[0:4]) # rect
            img.draw_cross(max_blob[5], max_blob[6]) # cx, cy
            ###hand
            hand.first_reset()
            hand.hand_down_two()
            hand.hand_forward(max_blob[3])
            hand.hand_up()
            p=3
            break
        else:
            p=1

    car_speed=car_speed_max
    k=1
    area=(0,0,160,120)
    ti=1
    ti_2=1
    while(True and p==3):
        pass
        clock.tick()
        img = sensor.snapshot()
        blobs = img.find_blobs([home_threshold])
        if blobs:
            pass
            ti=time_counter(ti)
            if ti>800:
                car_adjust()
                p=1
                break
            max_blob = find_max(blobs)
            img.draw_rectangle(max_blob[0:4]) # rect
            img.draw_cross(max_blob[5], max_blob[6]) # cx, cy
            x_error = max_blob[5]-80
            y_error = max_blob[3]-home_high
            x_output=x_pid.get_pid(x_error,1)
            y_output=y_pid.get_pid(y_error,1)
            if 85>max_blob[3]>70:
                x_range_home=30
            elif max_blob[3]>=85:
                x_range_home=10
            else:
                x_range_home=40

            if x_error<-x_range_home or x_error>x_range_home:
                car.run(-x_output,x_output)
            else:
                if -y_range_home<y_error<y_range_home:
                    p=4
                    car_stop(car_speed)
                    break
                else:
                    if 50>max_blob[3]>40:
                        car_speed=70
                    elif 60>max_blob[3]>=50:
                        car_speed=60
                    elif 70>max_blob[3]>=60:
                        car_speed=55
                    elif 80>max_blob[3]>=70:
                        car_speed=48
                    elif max_blob[3]>=80:
                        car_speed=40
                    else:
                        car_speed=100
                    car_move(y_error,y_range_home,car_speed)
        else:
            #car.run(car_turn_speed,-car_turn_speed)
            ti_2=time_counter(ti_2)
            if ti_2>500:
                if rand==0:
                    car.run(car_turn_speed,-car_turn_speed)
                else:
                    car.run(-car_turn_speed,car_turn_speed)
                time.sleep(2000)
                car.run(car_speed,car_speed)
                time.sleep(1000)
                car.run(0,0)
                p=1
                break
            if rand==0:
                car.run(-car_turn_speed,car_turn_speed)
            else:
                car.run(car_turn_speed,-car_turn_speed)
    car_speed=car_speed_max
    while(True and p==4):
        hand.hand_shot_ready()
        #hand.hand_shot_ready_more()
        hand.hand_shot()
        car_back()
        p=1
        break

