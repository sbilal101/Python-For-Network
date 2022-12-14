#! /usr/bin/env  python
# -*- coding: utf-8 -*-
"""
Task 18.1
Create send_show_command function.
The function connects via SSH (using netmiko) to ONE device and executes
the specified command.
Function parameters:
* device - a dictionary with parameters for connecting to a device
* command - the command to be executed
The function should return a string with the command output.
The script should send command command to all devices from the devices.yaml file
using the send_show_command function (this part of the code is written).
"""
import yaml
from netmiko import (ConnectHandler,NetmikoTimeoutException,NetmikoAuthenticationException,)
from pprint import pprint
def send_show_command(device,command):
    result={}
    
    with ConnectHandler(**device) as ssh:
         ssh.enable()
         result[command] =ssh.send_command(command)
            
    return result
   
if __name__ == "__main__":
    cmd = "sh ip int br | ex un"
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        pprint(send_show_command(dev, cmd),width=120)
