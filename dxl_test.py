from dxl_control.Ax12 import Ax12

# create motor object
my_dxl = Ax12(9)

# connecting
Ax12.open_port()
Ax12.set_baudrate()


def user_input():
    """ Check to see if user wants to continue """
    ans = input('Continue? : y/n ')
    if ans == 'n':
        return False
    else:
        return True


def test_pos(motor_object):
    bool_test = True
    while bool_test:
        motor_object.get_position()
        # desired angle input
        input_pos = int(input("input pos: "))
        motor_object.set_position(input_pos)
        bool_test = user_input()

test_pos(my_dxl)




# disconnect
my_dxl.disable_torque()
Ax12.close_port()
