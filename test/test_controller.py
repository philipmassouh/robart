from server.controller.controllers import RobotController, TextRobot


def test_can_instantiate_robot_controller():
    RobotController(TextRobot, name='Robart')


def test_drive_forward():
    controller = RobotController(TextRobot, name='Robart')
    output = controller.drive_forward_(100, 10)
    assert "Driving forward" in output
    assert "distance 100" in output
    assert "speed 10" in output
