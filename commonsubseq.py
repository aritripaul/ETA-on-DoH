#Author: Aritri Paul
#To execute the code, type the following command in your terminal: python3 commonsubseq.py <output_folder_name>

import sys
import os
import itertools

foldername = sys.argv[1]   #Takes folder name(here, 'Output') as command line input
file_obj=open("Commonsubsq.txt","a")

count=0                                 #counts number of files in the folder given by the user   
for file in os.listdir(foldername):
   count+=1

for i in range(1,count+1):
    file_obj.write(str(i))
    file_obj.write("--")
    readfile=open("Output/"+str(i)+".txt",'r')
    l=readfile.readlines()

    f=0
    list2=[]
    #l = [x for x in l if x != []]
    for j in range(len(l)):
        l[j]=l[j][1:-2]
        if(len(l[j])==0):
            f=1
            
      
    if(f):  #to remove elements from the list which have no sequence. For eg: the 4th sample of 18th url(line 4 of 18.txt)    
        list2 = [x for x in l if x]
        l=list2
        
    if(len(l)==0):
        file_obj.write("\n")
        continue

    
    listoflists=[]  #to convert each string of the 10 strings in the .txt file to lists ans store them in a list of lists
    for j in range(len(l)):
        li=list(l[j].split(","))
        listoflists.append(li)

    n=len(listoflists)
    s=listoflists[0]
    length=len(s)
    

    res=[]      #to store substring with max length
    multiple=[]  #to store multiple results with maximum length

    for j in range(length):
        for x in range(j+1,length+1):
            stem=s[j:x]
            
            k=1
            flag=True
            for k in range(1,n):
                if(not(', '.join(map(str, stem)) in ', '.join(map(str, listoflists[k])))): #check whether the subsequence is present in all strings or not
                    flag=False
                    break

            if(flag and len(res)<len(stem)): #find max subsequence
                res=stem
        
            elif(flag and len(res)==len(stem)): #store all subsequences of max length
                multiple.append(stem)

    ans=[]  #store all subsequences which have length same as res(since res will store max subsequence)
    ans.append(res)
    for i in range(len(multiple)):
        if(len(multiple[i])==len(res)):
            ans.append(multiple[i])
    
    ans.sort() 

    file_obj.write("[")   #write the first element of ans in the file
    for item in range(len(ans[0])-1):
        file_obj.write("%s," % ans[0][item])
    file_obj.write("%s]"% ans[0][len(ans[0])-1])


    for j in range(1,len(ans)):  #compare the rest of the subsequences in ans, to avoid duplicates
        if(len(ans[j])>2):
            if(ans[j]!=ans[j-1]):
                file_obj.write("[")
                for item in range(len(ans[j])-1):
                    file_obj.write("%s," % ans[j][item])
                file_obj.write("%s]"%ans[j][len(ans[j])-1])
            

    file_obj.write("\n")


   





