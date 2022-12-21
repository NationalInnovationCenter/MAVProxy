#!/usr/bin/env python
import pymavlink.dialects.v20.nicnepal as nicnepal
from MAVProxy.modules.lib import mp_module


class NICNepalModule(mp_module.MPModule):
    def __init__(self, mpstate):
        super().__init__(mpstate, "nicnepal", "NIC Nepal test module")
        self.add_command('actuator', self.actuator_cmd, 'Send actuator turn on command')
        self.add_command('sensor', self.sensor_cmd, 'Show NIC sensor value')
        self.actuator_state = None
        self.sensor_value = None

    def mavlink_packet(self, m):
        '''handle a mavlink packet'''
        message_type = m.get_type()
        if message_type == 'MAV_NIC_ACTUATOR_STATE':
            self.actuator_state = m.actuator_output_status
            print(f'Update for actuator received, value: {self.actuator_state}')
        elif message_type == 'MAV_NIC_SENSOR_STATE':
            self.sensor_value = m.sensor_value
            print(f'Update for sensor received, value: {self.sensor_value}')
        else:
            pass

    def actuator_cmd(self, args):
        mav = self.master
        if len(args) == 0:
            if self.actuator_state is None:
                print('No actuator update messages have been received')
            elif self.actuator_state == 1:
                print('Actuator is ON')
            elif self.actuator_state == 0:
                print('Actuator is OFF')
            else:
                print('The actuator state has an invalid value')
        elif args[0] == 'off':
            message = nicnepal.MAVLink_mav_cmd_nic_actuator_actuate_message(0)
            mav.mav.send(message)
            print("Actuator Off message sent")
        elif args[0] == 'on':
            message = nicnepal.MAVLink_mav_cmd_nic_actuator_actuate_message(1)
            mav.mav.send(message)
            print("Actuator On message sent")
        else:
            print("Usage: actuator on|off (Turn the actuator on or off)")

    def sensor_cmd(self):
        if self.sensor_value is None:
            print('No updates for sensor value have been received')
        else:
            print(f'Sensor value: {self.sensor_value}')


def init(mpstate):
    '''initialise module'''
    return NICNepalModule(mpstate)
