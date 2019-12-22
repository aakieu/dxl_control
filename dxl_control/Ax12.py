# import module as alias
from dynamixel_sdk import *                    # Uses Dynamixel SDK library
from dxl_control.ax12_control_table import *  # Uses ax12 Control Table


class Ax12:
    """ Class for Dynamixel AX12A motors."""
    PROTOCOL_VERSION = 1.0
    BAUDRATE = 1000000             # Dynamixel default baudrate
    DEVICENAME = '/dev/ttyUSB0'           # Default COM Port
    portHandler = PortHandler(DEVICENAME)   # Initialize Ax12.PortHandler instance
    packetHandler = PacketHandler(PROTOCOL_VERSION)  # Initialize Ax12.PacketHandler instance
    # Dynamixel will rotate between this value
    MIN_POS_VAL = 0
    MAX_POS_VAL = 1023

    @classmethod
    def open_port(cls):
        if cls.portHandler.openPort():
            print("Succeeded to open the port")
        else:
            print("Failed to open the port")
            print("Press any key to terminate...")
            quit()

    @classmethod
    def set_baudrate(cls):
        if cls.portHandler.setBaudRate(cls.BAUDRATE):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            print("Press any key to terminate...")
            quit()

    @classmethod
    def close_port(cls):
        # Close port
        cls.portHandler.closePort()
        print('Successfully closed port')

    def __init__(self, motor_id):
        """Initialize motor id"""
        self.id = motor_id

    def set_register1(self, reg_num, reg_value):
        dxl_comm_result, dxl_error = Ax12.packetHandler.write1ByteTxRx(
            Ax12.portHandler, self.id, reg_num, reg_value)
        Ax12.check_error(dxl_comm_result, dxl_error)

    def set_register2(self, reg_num, reg_value):
        dxl_comm_result, dxl_error = Ax12.packetHandler.write2ByteTxRx(
            Ax12.portHandler, self.id, reg_num, reg_value)
        Ax12.check_error(dxl_comm_result, dxl_error)

    def get_register1(self, reg_num):
        reg_data, dxl_comm_result, dxl_error = Ax12.packetHandler.read1ByteTxRx(
            Ax12.portHandler, self.id, reg_num)
        Ax12.check_error(dxl_comm_result, dxl_error)
        return reg_data

    def get_register2(self, reg_num_low):
        reg_data, dxl_comm_result, dxl_error = Ax12.packetHandler.read2ByteTxRx(
            Ax12.portHandler, self.id, reg_num_low)
        Ax12.check_error(dxl_comm_result, dxl_error)
        return reg_data

    def enable_torque(self):
        """Enable torque for motor."""
        self.set_register1(ADDR_AX_TORQUE_ENABLE, TORQUE_ENABLE)
        print(self.get_register1(ADDR_AX_TORQUE_ENABLE))
        # print("Torque has been successfully enabled for dxl ID: %d" % self.id)

    def disable_torque(self):
        """Disable torque."""
        self.set_register1(ADDR_AX_TORQUE_ENABLE, TORQUE_DISABLE)
        print(self.get_register1(ADDR_AX_TORQUE_ENABLE))
        # print("Torque has been successfully disabled for dxl ID: %d" % self.id)

    def set_position(self, dxl_goal_position):
        """Write goal position."""
        self.set_register2(ADDR_AX_GOAL_POSITION_L, dxl_goal_position)
        print("Position of dxl ID: %d set to %d " %
              (self.id, dxl_goal_position))

    def set_moving_speed(self, dxl_goal_speed):
        """Set the moving speed to goal position [0-1023]."""
        self.set_register2(ADDR_AX_GOAL_SPEED_L, dxl_goal_speed)
        print("Moving speed of dxl ID: %d set to %d " %
              (self.id, dxl_goal_speed))

    def get_position(self):
        """Read present position."""
        dxl_present_position = self.get_register2(ADDR_AX_PRESENT_POSITION_L)
        print("ID:%03d  PresPos:%03d" % (self.id, dxl_present_position))
        return dxl_present_position

    def get_present_speed(self):
        """Returns the current speed of the motor."""
        present_speed = self.get_register2(ADDR_AX_PRESENT_SPEED_L)
        return present_speed

    def get_moving_speed(self):
        """Returns moving speed to goal position [0-1023]."""
        moving_speed = self.get_register2(ADDR_AX_GOAL_SPEED_L)
        return moving_speed

    def led_on(self):
        """Turn on Motor Led."""
        self.set_register1(ADDR_AX_LED, True)

    def led_off(self):
        """Turn off Motor Led."""
        self.set_register1(ADDR_AX_LED, False)

    def get_load(self):
        """Returns current load on motor."""
        dxl_load = self.get_register2(ADDR_AX_PRESENT_LOAD_L)
        # CCW 0-1023 # CW 1024-2047
        return dxl_load

    def get_temperature(self):
        """Returns internal temperature in units of Celsius."""
        dxl_temperature = self.get_register2(ADDR_AX_PRESENT_TEMPERATURE)
        return dxl_temperature

    def get_voltage(self):
        """Returns current voltage supplied to Motor in units of Volts."""
        dxl_voltage = (self.get_register1(ADDR_AX_PRESENT_VOLTAGE))/10
        return dxl_voltage

    def set_torque_limit(self, torque_limit):
        """Sets Torque Limit of Motor."""
        self.set_register2(ADDR_AX_TORQUE_LIMIT_L, torque_limit)

    def get_torque_limit(self):
        """Returns current Torque Limit of Motor."""
        dxl_torque_limit = self.get_register2(ADDR_AX_TORQUE_LIMIT_L)
        return dxl_torque_limit

    def is_moving(self):
        """Checks to see if motor is still moving to goal position."""
        dxl_motion = self.get_register1(ADDR_AX_MOVING)
        return dxl_motion

    @staticmethod
    def check_error(comm_result, dxl_err):
        if comm_result != COMM_SUCCESS:
            print("%s" % Ax12.packetHandler.getTxRxResult(comm_result))
        elif dxl_err != 0:
            print("%s" % Ax12.packetHandler.getRxPacketError(dxl_err))
