from robot_controller import RobotController

controller = RobotController()
controller.run('auto_mcl', '/home/raspberrypi/capstone-design-project/raspberrypi/board/path_simple.json', '/home/raspberrypi/capstone-design-project/raspberrypi/board/map_simple.json')