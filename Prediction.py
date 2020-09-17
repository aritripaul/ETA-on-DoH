#Author : Aritri Paul
#To execute the code, type the following command in your terminal: python3 Prediction.py <pcap file name>

import sys
import pyshark
import os
import collections


def check_exists(l, lookup_list):
    check = True
    for i in lookup_list:
        try:
            index = l.index(i) 
            l = l[index+1:]
        except ValueError:
            check = False 
            break 
    return check

def isSubArray(test_dns, each_dns, n, m): 
    i = 0
    j = 0
    while (i < n and j < m): 
        if (test_dns[i] == each_dns[j]): 
            i += 1
            j += 1 
  
            if (j == m): 
                return True 
       
        else: 
            i = i - j + 1
            j = 0 
          
    return False


file=sys.argv[1]
file=file+".raw"   #Takes the pcap file as command line input


path_to_pcap=os.path.join(os.curdir, file)
cmd = 'tshark -T fields -e tls.record.length -r '+ path_to_pcap 
tmpresult = os.popen(cmd).read().rstrip().rsplit('\n')
temp = []
for item in tmpresult:
    temp.append(item.split('\t'))



result=[]
for each in range(len(temp)):
    for element in range(len(temp[each])):
        result.append(temp[each][element])


sizefile=open('sizeset.txt','r')
sizeset=set()
for line in sizefile:
    number=0
    for element in line:
        if(element==' '):
            sizeset.add(number)
            number=0
        else:
            number=(number*10)+int(element)


dns=[]
for i in range(len(result)):
    result[i]=(result[i].split(','))
    for j in range(len(result[i])):
        if(result[i][j]):
            if(int(result[i][j]) in sizeset):
                dns.append(result[i][j])




######### FIRST CHECK ON URLS ON THE BASIS OF SUBSEQUENCES #######

dict={}
countarray=[]
count=0
st=set()

text_file=open("Commonsubsq.txt",'r')
for line in text_file:
    count+=1 
   
    for i in range(len(line)):
        if(line[i]=='['):
            array=[]
            s=""
            i+=1
            while(line[i]!=']'):
                s=s+line[i]
                i+=1

            
            array=list(s.split(',')) 
            
            if(check_exists(dns,array)):
                st.add(count)


######### SECOND CHECK ON URLS ON THE BASIS OF MAXIMUM LENGTH OF SUBARRAY #######

count=0
subarray={}
maxl=-1
text_file=open("Commonsubsq.txt",'r')
for line in text_file:
    count+=1
    
    if(count in st):
        
        ans=-1
        for i in range(len(line)):
            if(line[i]=='['):
                array=[]
                s=""
                i+=1
                while(line[i]!=']'):
                    s=s+line[i]
                    i+=1

                
                array=list(s.split(','))
                
                if(isSubArray(dns,array,len(dns),len(array))):
                    subarray[count]=len(array)
                    maxl=max(maxl,len(array))
                        
  
st=set()
for key in subarray:
    if(subarray[key]==maxl):
        st.add(key)

        
######### PRINTING PREDICTED URLS #######

url_count=0
ans=0
url_open=open("url.txt",'r')
for line in url_open:
    url_count+=1
    if(url_count in st):
        print(line)
        ans+=1




      







       
       










    
  
    


