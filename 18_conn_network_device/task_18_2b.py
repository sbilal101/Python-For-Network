#! /usr/bin/env python
""" Task 18.2b
Copy the send_config_commands function from task 18.2a and add error checking.
When executing each command, the script should check the output for the following errors: Invalid
input detected, Incomplete command, Ambiguous command
If an error occurs while executing any of the commands, the function should print a message to
the stdout with information about what error occurred, in which command and on which device,
for example: The “logging” command was executed with the error “Incomplete command.” on the
device 192.168.100.1
Errors should always be printed, regardless of the value of the log parameter. At the same time,
the log parameter should still control whether the message “Connecting to 192.168.100.1…” will be
displayed.
Send_config_commands should now return a tuple of two dictionaries:
• the first dict with the output of commands that were executed without error
• second dict with the output of commands that were executed with errors
In both dictionaries:
• key - command
• value - output with command execution

"""
import yaml
from netmiko import (ConnectHandler,NetmikoTimeoutException,NetmikoAuthenticationException,)
from pprint import pprint
def send_config_commands(device,config_commands,log=True):
    result={}
    bad={}
    
    if log :
        print("connecting to ", device['host'] , "....")
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            
            for command in config_commands:
                
                output=ssh.send_config_set(command)
                if "Invalid input detected" in output:
                    print(command+ ' command was executed with error "Invalid input detected" on device ' + device['host'])
                    bad[command]=output
                elif "Incomplete command" in output:
                    print(command+ ' command was executed with error "Incomplete command" on device ' + device['host'])
                    bad[command]=output
                elif "Ambiguous command" in output:
                    print(command+ ' command was executed with error "Ambiguous command" on device ' + device['host'])
                    bad[command]=output
                else:    
                    result[command] = output
                
        return result,bad
        
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)
        
if __name__ == "__main__":
    commands = ['logging ','logging buffered 20010','no logging console']
    with open('devices.yaml') as f:
        devices=yaml.safe_load(f)
        for device in devices:
            good, bad =send_config_commands(device, commands)
            
        print(good.keys())
    
