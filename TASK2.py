
import glob
import re
import csv
def parse_sh_version(sh_ver):
    
    #process output from show version of router using Regex
      
    regx=re.compile('\d+\.\d+\(\d+\)\w+')
    x= regx.search(sh_ver).group()
    ios= x if x else 'No IOS'
    
    regx=re.compile('"flash\S+')
    y=eval(regx.search(sh_ver).group())
    image= y if y else 'No Image'
    
    regx=re.compile('uptime is \S+ \S+ \S+ \S+ \S+ \S+ \S+ \S+')
    z=(regx.search(sh_ver).group()).lstrip('uptime is ')
    uptime=z if z else "Not Running"
    
    
    rtn=(ios,image,uptime)
    
    return rtn
    
    
    
def write_inventory_to_csv(data_fileName,csv_fileName):
    #process from each file sh ver output. file name like sh_ver_r1.txt,sh_ver_r2.txt
    inventory=[]
    host=[]
    for i in range(len(data_fileName)):
        with open(data_fileName[i]) as f:
            file_content=f.read()
            #Extract Host name from the Filename
            host.append(data_fileName[i].strip('.txt').split('_')[-1])
            #call parse_sh_version function and convert the retun tuple vlaue to List
            T=list(parse_sh_version(file_content))
            #Insert the host name 
            T.insert(0,host[i])
            #Reverse the order of the list
            inventory.append(T)
            
            
    Header=('Hostname','ios','image','uptime')
    
    inventory.append(Header)
    inventory.reverse()
    host.reverse()
    
  
    #call parse_sh_version().routers_inventory.csv-->columns hostname,ios,image,uptime
    with open(csv_fileName,'w') as f:
        writer=csv.writer(f)
        for row in inventory:
            writer.writerow(row)
            
           
   
   #Main Function
    
if __name__== "__main__":
    
    file_lst=[]
    csv_file='router_inventory.csv'
# get input files or ask for file location
    for name in glob.glob('sh_ver_r?.txt'):
        file_lst.append(name)
    

    write_inventory_to_csv(file_lst,csv_file)
