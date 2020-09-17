#Author: Aritri Paul
#To execute the code, type the following command in your terminal: python3 Sequence.py

import sys
import pyshark
import os
import collections


for file in os.listdir(os.curdir):
    if file.endswith(".log"):
        key=os.path.join(os.curdir, file)            #path to key file is determined


url_count=0

path=os.path.join(os.curdir,"Output")
os.mkdir(path)

with open('url.txt', 'r') as f:
    for line in f:
        url_count += 1


for i in range(1,url_count+1):
    for j in range(0,10):
        file=str(i)+"_"+str(j)+".raw"
        path_to_pcap=os.path.join(os.curdir, file)
        cmd = 'tshark -o "tls.keylog_file:'+key+'" -Y "tcp.dstport==443 && dns" -T fields -e tls.record.length -r '+ path_to_pcap 
        tmpresult = os.popen(cmd).read().rstrip().rsplit('\n')
        temp = []
        for item in tmpresult:
            temp.append(item.split('\t'))

        result=[]
        for each in range(len(temp)):
            for element in range(len(temp[each])):
                result.append(temp[each][element])

       
        output_file=open("Output/"+str(i)+".txt",'a')
        output_file.write("[")
        output_file.writelines("%s,"% result[element] for element in range(len(result)-1)) 
        output_file.write("%s]\n"%result[len(result)-1])    

        if(j==0):
            command="Created "+str(i)+".txt.\nWriting to "+str(i)+".txt.."
            print(command)

        if(j==9):
            print("Done.")
            
        output_file.close()










    
  
    


