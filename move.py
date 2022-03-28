import sensor, image, time,random
import car
import  math


sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # use RGB565.
sensor.set_framesize(sensor.QQVGA) # use QQVGA for speed.
sensor.skip_frames(60) # Let new settings take affect.
sensor.set_auto_whitebal(False) # turn this off.
clock = time.clock() # Tracks FPS.


red_threshold     = (46, 77, 53, 111, -11, 64)
green_threshold   = (32, 92, -69, -34, -1, 39)
#green_threshold   = (32, 100, -77, -24, -24, 22)
blue_threshold    = (32, 77, -12, 27, -69, -25)
ball_threshold    =  red_threshold
home_threshold    =  green_threshold
ball_high=30
home_high=90

car_speed=50
car_turn_speed=50
x_range=40
y_range=15
x_range_home=10
y_range_home=10

def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob[2]*blob[3] > max_size:
            max_blob=blob
            max_size = blob[2]*blob[3]
    return max_blob

def car_rotate(x_error,x_range):
    pass
    print('旋转')
    if x_error<-10:
        car.run(car_speed,-car_speed)
    elif x_error>x_range:
        car.run(-car_speed,car_speed)


def car_move(y_error,y_range):
    pass
    print('移动')
    if y_error<0:
        car.run(car_speed,car_speed)
    elif y_error>y_range:
        car.run(-car_speed,car_speed)


def car_back():


while(True):
    while(True):
        clock.tick()
        img = sensor.snapshot()
        blobs = img.find_blobs([ball_threshold])
        if blobs:
            max_blob = find_max(blobs)
            x_error = max_blob[5]-80
            y_error = max_blob[3]-ball_high
            img.draw_rectangle(max_blob[0:4]) # rect
            img.draw_cross(max_blob[5], max_blob[6]) # cx, cy
            print(x_error,y_error)
            if x_error<-x_range or x_error>x_range:
                car_rotate(x_error,x_range)
            else:
                if 0<y_error<y_range:
                    break
                else:
                    car_move(y_error,y_range)
        else:
            car.run(-car_turn_speed,car_turn_speed)


    while(True):
        pass
        clock.tick()
        img = sensor.snapshot()
        blobs = img.find_blobs([home_threshold])
        if blobs:
            max_blob = find_max(blobs)
            x_error = max_blob[5]-80
            y_error = max_blob[3]-home_high
            if x_error<-x_range_home or x_error>x_range_home:
                car_rotate(x_error,x_range_home)
            else:
                if 0<y_error<y_range_home:
                    break
                else:
                    car_move(y_error,y_range_home)
        else:
            car.run(car_turn_speed,-car_turn_speed)

