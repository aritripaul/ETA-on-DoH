#Author: Aritri Paul

import sys
import pyshark

text_file=open("Commonsubsq.txt",'r')
sizeset=set()
for line in text_file:
    for i in range(len(line)):
        if(line[i]=='['):
            array=[]
            s=""
            i+=1
            while(line[i]!=']'):
                s=s+line[i]
                i+=1
  
            array=list(s.split(','))
            for i in array:        #add all sizes into a set, to find the final set of distinct DOH packet sizes
                sizeset.add(i)


writef=open('sizeset.txt','w')
for i in sizeset:
    writef.write(str(i)+" ")
    

            

