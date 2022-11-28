#! /usr/bin/env python
""" Task 18.2 and  Task 18.2
Create send_config_commands function
The function connects via SSH (using netmiko) to ONE device and executes a list of commands in
configuration mode based on the passed arguments.
Function parameters:
• device - a dictionary with parameters for connecting to a device
• config_commands - list of configuration commands to be executed
The function should return a string with the results of the command 

Task 18.2a
Copy the send_config_commands function from job 18.2 and add the log parameter. The log parameter
controls whether information is displayed about which device the connection is to:
• if log is equal to True - information is printed
• if log is equal to False - information is not printed
By default, log is equal to True.
"""
import yaml
from netmiko import (ConnectHandler,NetmikoTimeoutException,NetmikoAuthenticationException,)
from pprint import pprint
def send_config_commands(device,config_commands,log=True):
    result={}
    if log :
        print("connecting to ", device['host'] , "....")
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            for command in config_commands:
                output=ssh.send_config_set(command)
                
                result[command] = output
                
        return result
        
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)
        
if __name__ == "__main__":
    commands = ['logging 172.16.2.74','logging buffered 20010','no logging console']
    with open('devices.yaml') as f:
        devices=yaml.safe_load(f)
        for device in devices:
            pprint(send_config_commands(device, commands,log=False),width=120)
    
