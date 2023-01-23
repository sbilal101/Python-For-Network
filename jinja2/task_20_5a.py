# -*- coding: utf-8 -*-
"""
Task 20.5a

Create a configure_vpn function that uses the templates from task 20.5
to configure VPN on routers based on the data in the data dictionary.

Function parameters:
* src_device_params - dictionary with connection parameters for device 1
* dst_device_params - dictionary with connection parameters for device 2
* src_template - a template that creates the configuration for side 1
* dst_template - a template that creates the configuration for side 2
* vpn_data_dict - a dictionary with values to be substituted into templates

The function should configure the VPN based on templates and data on each
device using netmiko. The function returns a tuple with the output of commands
from two routers (the output returned by the netmiko send_config_set method).
The first element of the tuple is the output from the first device (string),
the second element of the tuple is the output from the second device.

In this task, the data dictionary does not specify the Tunnel interface
number to use. The number must be determined independently based on information
from the equipment. If the router does not have Tunnel interfaces, take
the number 0, if there is, take the nearest free number, but the same for two routers.

For example, if the src router has the following interfaces: Tunnel1, Tunnel4.
And on the dst router are: Tunnel2, Tunnel3, Tunnel8.
The first free number that is the same for two routers will be 5.
And you will need to configure the Tunnel 5 interface.

For this task, the test verifies that the function works on the first
two devices from the devices.yaml file. And it checks that the output contains
commands for configuring interfaces, but does not check the configured tunnel
numbers and other commands. The tunnels must be configured, but the test has been
simplified so that there are fewer constraints on the task.

"""
import re
from netmiko import ConnectHandler
import yaml
from task_20_5 import create_vpn_config
data = {
    "tun_num": None,
    "wan_ip_1": "192.168.100.1",
    "wan_ip_2": "192.168.100.2",
    "tun_ip_1": "10.0.1.1 255.255.255.252",
    "tun_ip_2": "10.0.1.2 255.255.255.252",
}


def connect_device(device):
    ssh = ConnectHandler(**device)
    ssh.enable()
    return ssh


def get_free_interface(src, dst):
    regex = re.findall(r"Tunnel(\d+)", src + dst)
    nums = [int(num) for num in regex]
    if not nums:
        return 0
    diff = set(range(min(nums), max(nums) + 1)) - set(nums)
    if diff:
        return min(diff)
    else:
        return max(diff) + 1


def create_vpn(src_device_params, dst_device_params, src_template, dst_template, vpn_data_dict):

    with ConnectHandler(**src_device_params) as src, ConnectHandler(**dst_device_params) as dst:
        src.enable()
        dst.enable()
        src_tun = src.send_command('show run | include ^interface Tunnel')
        dst_tun = dst.send_command('show run | include ^interface Tunnel')
        tun_num = get_free_interface(src_tun, dst_tun)
        vpn_data_dict['tun_num'] = tun_num
        vpn1, vpn2 = create_vpn_config(src_template, dst_template, data)
        src_conf = src.send_config_set(vpn1.split('\n'))
        dst_conf = dst.send_config_set(vpn2.split('\n'))
        return src_conf, dst_conf


if __name__ == '__main__':
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
    d1, d2 = devices[:2]
    create_vpn(d1, d2, 'templates/gre_ipsec_vpn_1.txt', 'templates/gre_ipsec_vpn_2.txt', data)
