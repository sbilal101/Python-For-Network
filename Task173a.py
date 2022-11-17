#! /usr/bin/env python
import re
import glob
from pprint import pprint
list_of_files=[]

def generate_topology_from_cdp():

    #Read sh CDP neighbor files
    result={}
    host_regx=re.compile('\w+\d+')
    nei_regx=re.compile('\w+\d+')
    port_regx=re.compile('\w\w\w +\d+\/\S')
    #rport_regx=re.compile('\w\w\w +\d+\/\S')
    
    for i in range(len(list_of_files)):
    
        with open(list_of_files[i]) as f:
    
            host=host_regx.search(f.readline()).group()
                 
            for line in f:
                port = port_regx.findall(line)
               
                if not port :
                     continue
                else:
                    #port=port.group()       
                    nei=nei_regx.search(line).group()
                    port = port_regx.findall(line)
                   
           
        
                    if host not in result:
                        #result={host:{lport:{nei:rport}}}
                        result={host:{port[0]:{nei:port[1]}}}
                    else:
                        result[host][port[0]]={nei:port[1]}
                

    pprint(result)



   
    
        
    
    #save to file. save_to_file is the file name 


if __name__== "__main__":
    #get cdp files
    for name in glob.glob('sh_cdp_n_*.txt'):
        list_of_files.append(name)
    
    
    generate_topology_from_cdp()
