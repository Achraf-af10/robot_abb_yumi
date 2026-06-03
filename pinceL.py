# pinceL.py
import time

def openL(robot, position=25):
    robot.set_rapid_variable("gripPosL", str(position), "T_ROB_L")
    robot.set_rapid_variable("cmdGripL", "1", "T_ROB_L")
    time.sleep(2)

def closeL(robot, position=0):
    robot.set_rapid_variable("gripPosL", str(position), "T_ROB_L")
    robot.set_rapid_variable("cmdGripL", "1", "T_ROB_L")
    time.sleep(2)