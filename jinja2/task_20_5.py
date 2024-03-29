# -*- coding: utf-8 -*-
"""
Task 20.5

Create template templates/gre_ipsec_vpn_1.txt and templates/gre_ipsec_vpn_2.txt
that generate IPsec over GRE configuration between two routers.

The templates/gre_ipsec_vpn_1.txt template creates the configuration for one
side of the tunnel, and templates gre_ipsec_vpn_2.txt for the other.

Examples of the final configuration that should be generated from templates
in the files: cisco_vpn_1.txt and cisco_vpn_2.txt.

Templates must be created manually by copying parts of the config into
the corresponding templates.

Create a create_vpn_config function that uses these templates to generate
a VPN configuration based on the data in the data dictionary.

Function parameters:
* template1 - the name of the template file that creates the configuration
  for one side of the tunnel
* template2 - the name of the template file that creates the configuration
  for the second side of the tunnel
* data_dict - a dictionary with values to be substituted into templates

The function must return a tuple with two configurations (strings) that are
derived from templates.

Examples of VPN configurations that the create_vpn_config function
should return in the cisco_vpn_1.txt and cisco_vpn_2.txt files.
"""

from jinja2 import Environment, FileSystemLoader
import os

data = {
    "tun_num": 10,
    "wan_ip_1": "192.168.100.1",
    "wan_ip_2": "192.168.100.2",
    "tun_ip_1": "10.0.1.1 255.255.255.252",
    "tun_ip_2": "10.0.1.2 255.255.255.252",
}


def create_vpn_config(template1, template2, data_dict):
    template_dir1, temp_file1 = os.path.split(template1)
    env = Environment(loader=FileSystemLoader(template_dir1), trim_blocks=True, lstrip_blocks=True)
    temp1 = env.get_template(temp_file1)

    template_dir2, temp_file2 = os.path.split(template2)
    env = Environment(loader=FileSystemLoader(template_dir2), trim_blocks=True, lstrip_blocks=True)
    temp2 = env.get_template(temp_file2)
    return temp1.render(data_dict), temp2.render(data_dict)
    # this is how a function call should look


if __name__ == "__main__":
    data_file = "data_files/add_vlan_to_switch.yaml"
    template_file1 = "templates/gre_ipsec_vpn_1.txt"
    template_file2 = "templates/gre_ipsec_vpn_2.txt"
    '''
    with open(data_file) as f:
        data = yaml.safe_load(f)
 '''
    vpn1, vpn2 = create_vpn_config(template_file1, template_file2, data)
    print(vpn1)
    print(vpn2)
