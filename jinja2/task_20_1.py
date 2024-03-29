# -*- coding: utf-8 -*-
"""
Task 20.1

Create generate_config function.

Function parameters:
* template - path to the template file (for example, "templates/for.txt")
* data_dict - a dictionary with values to be substituted into the template

The function should return the generated configuration string.

Check the operation of the function on the templates/for.txt template
and data from the data_files/for.yml file.

An important nuance: you need to get the directory from the template parameter,
you cannot specify the current directory in the FileSystemLoader - that is,
DO NOT do this: FileSystemLoader(".").
Specifying the current directory will break the work of other tasks/tests.
"""
import yaml
from jinja2 import Environment,FileSystemLoader
import sys
import os

def generate_config(template, data_dict):
    template_dir, template_file = os.path.split(template)
    env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True)
    temp=env.get_template(template_file)
    return temp.render(data_dict)
    # this is how a function call should look
if __name__ == "__main__":
    data_file = "data_files/add_vlan_to_switch.yaml"
    template_file = "templates/add_vlan_to_switch.txt"
    with open(data_file) as f:
        data = yaml.safe_load(f)

    print(generate_config(template_file, data))
