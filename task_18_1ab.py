#! /usr/bin/env  python
# -*- coding: utf-8 -*-
"""
Task 18.1a
Copy the send_show_command function from task 18.1 and rewrite it to handle the exception that
is thrown on authentication failure on the device.
When an error occurs, an exception message should be printed to stdout.
To verify, change the password on the device or in the devices.yaml file.

Task 18.1b
Copy the send_show_command function from task 18.1a and rewrite it to handle not only the exception
that is raised when authentication fails on the device, but also the exception that is raised
when the IP address of the device is not available.
When an error occurs, an exception message should be printed to standard output.
To check, change the IP address on the device or in the devices.yaml file.

"""
import yaml
from netmiko import (ConnectHandler,NetmikoTimeoutException,NetmikoAuthenticationException,)
from pprint import pprint
def send_show_command(device,commands):
    result={}
    try:
        with ConnectHandler(**device) as ssh:
             ssh.enable()
             output=ssh.send_command(command)
             result[command] = output
                
        return result
        
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)


if __name__ == "__main__":
    command = "sh ip int br | ex down"
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        pprint(send_show_command(dev, command),width=120)
