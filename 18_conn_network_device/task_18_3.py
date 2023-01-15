#! /usr/bin/env python
"""
Task 18.3
Create a send_commands function (use netmiko to connect via SSH).
Function parameters:
• device - a dictionary with parameters for connecting to one device
• show - one show command (string)
• config - a list with commands to be executed in configuration mode
The show and config arguments should only be passed as keyword arguments. Passing these arguments
as positional should raise a TypeError exception. """
import yaml
from netmiko import (ConnectHandler,NetmikoTimeoutException,NetmikoAuthenticationException,)
from pprint import pprint
from task_18_1 import send_show_command
from task_18_2 import send_config_commands
from pprint import pprint

def send_commands(device,*,show=None,config=None):
    if show and config:
        raise ValueError("Only one of the show/config arguments can be passed")
    elif show:
        return send_show_command(device,show)
    elif config:
        return send_config_commands(device,config)
        
        
        
if __name__=="__main__":
    
    commands = ["logging 10.255.255.1", "logging buffered 20010", "no logging console"]
    command = "sh ip int br | ex down"
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    r1 = devices[0]
    
    pprint(send_commands(r1, config=commands),width=120)
    pprint(send_commands(r1, show=command),width=120)


