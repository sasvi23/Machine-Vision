from robot.dobot_controller import (
    ConnectRobot,
    SetupRobot,
    MoveJ,
    MoveL,
    WaitArrive,
    ControlDigitalOutput,
    DisconnectRobot,
    StartFeedbackThread
)

from time import sleep



def execute_pick_and_place(
    robot_targets,
    speed_ratio=50,
    acc_ratio=50,
    gripper_delay=0.8,
    safe_z=50,
    pick_z=-169.2,
    drop_x=325,
    drop_y=235,
    drop_z=-79,
    rotation=0,
):
    """Pick-and-place sequence with adjustable parameters.

    Parameters are provided so the calling code (CLI/UI) can tune performance.
    """

    print("\nConnecting to Dobot MG400...")

    dashboard, move, feed = ConnectRobot(ip="192.168.1.6")  # <-- CHANGE IP if needed
    feed_thread = StartFeedbackThread(feed)

    # apply speed/acceleration settings
    SetupRobot(dashboard, speed_ratio=speed_ratio, acc_ratio=acc_ratio)

    try:
        for target in robot_targets:
            print(target)

            X, Y = target["robot_coords"]

            print(f"\nPicking at X={X:.2f}, Y={Y:.2f}")

            # Move above object
            point_above = [X, Y, safe_z, rotation]
            MoveJ(move, point_above)
            WaitArrive(point_above)

            # Move down to pick
            point_pick = [X, Y, pick_z, rotation]
            MoveL(move, point_pick)
            WaitArrive(point_pick)

            # Close gripper (DO1 example)
            ControlDigitalOutput(dashboard, 1, 1)
            sleep(gripper_delay)

            # Move up
            MoveL(move, point_above)
            WaitArrive(point_above)

            # Move to drop position
            drop_above = [drop_x, drop_y, drop_z, rotation]
            MoveJ(move, drop_above)
            WaitArrive(drop_above)

            # Open gripper
            print("\nDO1 release.....")
            ControlDigitalOutput(dashboard, 1, 0)
            print("\nDO1 release.....")
            sleep(gripper_delay)

        print("\nAll targets processed successfully.")

    finally:
        DisconnectRobot(dashboard, move, feed, feed_thread)