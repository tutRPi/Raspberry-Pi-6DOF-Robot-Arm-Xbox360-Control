from RobotArm.Robot import Robot
from Xbox import xbox
import time

if __name__ == '__main__':
    joy = xbox.Joystick()
    robot = Robot()

    # initial states in percent
    states = [50, 50, 50, 80, 50, 50]
    for i, s in enumerate(states):
        robot.servo.move_servo_to_percent(i, s)

    # triggers for left/right thumbstick
    leftThumb, rightThumb = 0, 0
    leftFreeze, rightFreeze = False, False

    while not joy.Back():

        # Servo 0
        LB = joy.leftBumper()
        RB = joy.rightBumper()
        if LB > 0 or RB > 0:
            states[0] = max(0, min(100, int(states[0] + LB - RB)))
            robot.servo.move_servo_to_percent(0, states[0])

        # Servo 1
        up = joy.dpadUp()
        down = joy.dpadDown()
        if up > 0 or down > 0:
            states[1] = max(30, min(70, states[1] + 0.5*up - 0.5*down))
            robot.servo.move_servo_to_percent(1, states[1])

        # Servo 2
        BA = joy.A()
        BY = joy.Y()
        if BY > 0 or BA > 0:
            states[2] = max(20, min(80, states[2] + 0.5*BA - 0.5*BY))
            robot.servo.move_servo_to_percent(2, states[2])

        # Servo 3
        if joy.leftThumbstick() == 1 and leftThumb == 0:
            leftFreeze = not leftFreeze
        leftThumb = joy.leftThumbstick()
        if not leftFreeze:
            x,y = joy.leftStick()
            if abs(int(y*50.0)) > 0:
                states[3] = max(30, min(100, (65 + y*35 )))
                robot.servo.move_servo_to_percent(3, states[3])

        # Servo 4
        if joy.rightThumbstick() == 1 and rightThumb == 0:
            rightFreeze = not rightFreeze
        rightThumb = joy.rightThumbstick()
        if not rightFreeze:
            x,y = joy.rightStick()
            if abs(int(x*50)) > 0:
               states[4] = max(0, min(100, int(50 + x*50 )))
               robot.servo.move_servo_to_percent(4, states[4])


        # Hand / Servo 5
        RT = joy.rightTrigger()
        #if abs(int(RT*50)) > 0:
        states[5] = max(0, min(100, int(50 + RT*50 )))
        robot.servo.move_servo_to_percent(5, states[5])
        #print(states)
        time.sleep(0.02)

    joy.close()

