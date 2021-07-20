from server.controller.controllers import RobotController, TextRobot


def test_can_instantiate_robot_controller():
    RobotController(TextRobot, home_coords=(8.0, -1.0))


def test_drive_forward():
    controller = RobotController(TextRobot, home_coords=(8.0, -1.0))
    output = controller.drive(100, 10)
    assert "Driving" in output
    assert "distance 100" in output
    assert "speed 10" in output
