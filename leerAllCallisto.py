# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 17:51:32 2021

@author: Mario Fernández Ruiz
"""

import os
import urllib
from bs4 import BeautifulSoup
import requests

def listFD2(url):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser') #Devuelve todo el contenido de una página en formato html
    return [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith('.txt')]





#Se abre/crea el .csv para añadir la información de los events reports
nombreArchivo = "CallistoEvents"

fileOut= open('C:/Users/usuario/Desktop/e-Callisto/CallistoReports/'+nombreArchivo+'.csv', "w")
fileOut.close()
fileOut= open('C:/Users/usuario/Desktop/e-Callisto/CallistoReports/'+nombreArchivo+'.csv', "a")
fileOut.write("Year,Month,Day,Begin,End,Obs,Type\n")

url = 'http://soleil.i4ds.ch/solarradio/data/BurstLists/2010-yyyy_Monstein/2020/'
L = listFD2(url) #todos los reports de 2020

for i in range(len(L)):
    myfile = L[i].rsplit('/', 1)[1]
    myurl = url + myfile
    urllib.request.urlretrieve(myurl,myfile) #Descarga los events reports
    fileIn = open(myfile)
    rows = fileIn.readlines()
    if not "No" in rows[8]:
        year = myfile[11:15]
        month = myfile[16:18] 
        for j in range(8,len(rows)):              
            col=rows[j].rsplit()
            if (len(col)>1) and not ("##" in col[1]):                
                day = col[0][6:8]
                split = col[1].rsplit("-")
                begin = split[0].rsplit(":")[0]+split[0].rsplit(":")[1]
                end = split[1].rsplit(":")[0]+split[1].rsplit(":")[1]
                Type = col[2]
                for k in range(3,len(col)):
                    obs = col[k]
                    if "," in obs:
                        obs = obs.rstrip(obs[-1])
                    fileOut.write(year+','+month+','+day+','+begin+','+end+','+obs+','+Type+'\n')
 
            
 
#Repetimos todo para el año 2021. (Mejorar)    
url = 'http://soleil.i4ds.ch/solarradio/data/BurstLists/2010-yyyy_Monstein/2021/'
L = listFD2(url) #todos los reports de 2021

for i in range(len(L)):
    myfile = L[i].rsplit('/', 1)[1]
    myurl = url + myfile
    urllib.request.urlretrieve(myurl,myfile) #Descarga los events reports
    fileIn = open(myfile)
    rows = fileIn.readlines()
    if not "No" in rows[8]:
        year = myfile[11:15]
        month = myfile[16:18] 
        for j in range(8,len(rows)):              
            col=rows[j].rsplit()
            if ((len(col)>1)) and not ("##" in col[1]) and not (col[0]=="()" or col[0]=="[]" or col[0]=="???" or col[1]=="."):                
                day = col[0][6:8]
                if ("59.21" in col[1] or "18.21" in col[1]):
                    split = col[1].rsplit(".")
                else:
                    split = col[1].rsplit("-")
                
                if len(split)<2: #Literalmente esto solo pasa una vez. Es un error de Monstein :((((
                    if (col[0]=="20211218"):
                        split2 = col[1].rsplit(".")
                        begin = split2[0]
                        end = split2[1]
                    else:
                        split2 = col[1].rsplit(":",2)
                        begin = split2[0].rsplit(":")[0]+split2[0].rsplit(":")[1]
                        end = split2[1]+split2[2]
                elif ("_" in split[1]):
                    begin = split[0].rsplit(":")[0]+split[0].rsplit(":")[1]
                    end = split[1].rsplit("_")[0]+split[1].rsplit("_")[1]
                elif ("." in split[0]):
                    begin = split[0].rsplit(".")[0]+split[0].rsplit(".")[1]
                    end = split[1].rsplit(":")[0]+split[1].rsplit(":")[1]
                elif ("." in split[1]):
                    begin = split[0].rsplit(":")[0]+split[0].rsplit(":")[1]
                    end = split[1].rsplit(".")[0]+split[1].rsplit(".")[1]    
                else:
                    begin = split[0].rsplit(":")[0]+split[0].rsplit(":")[1]
                    end = split[1].rsplit(":")[0]+split[1].rsplit(":")[1]
                
                if (len(col)>2):
                    if ("," in col[2]):
                        Type= col[2].rsplit(",")[0]+"-"+col[2].rsplit(",")[1]
                    else:
                        Type=col[2]
                else:
                    Type = col[2]
              
                for k in range(3,len(col)):
                            obs = col[k]
                            if "," in obs:
                                obs = obs.rstrip(obs[-1])
                            if "," in obs:
                                obs1 = obs.rsplit(",")[0]
                                obs2 = obs.rsplit(",")[1]
                                fileOut.write(year+','+month+','+day+','+begin+','+end+','+obs1+','+Type+'\n')
                                fileOut.write(year+','+month+','+day+','+begin+','+end+','+obs2+','+Type+'\n')
                            else:
                                fileOut.write(year+','+month+','+day+','+begin+','+end+','+obs+','+Type+'\n')
"""                
                if (len(col)>19 and day=="01" and month=="03" and year=="2021"):
                    if ("," in col[19].rstrip(col[19][-1])):
                        for k in range(3,19):
                            obs = col[k]
                            if "," in obs:
                                obs = obs.rstrip(obs[-1])
                            fileOut.write(year+','+month+','+day+','+begin+','+end+','+obs+','+Type+'\n')
                        obs1 = col[19].rsplit(",")[0]
                        obs2 = col[19].rsplit(",")[1]
                        #obs2 = obs2.rstrip(obs2[-1])
                        fileOut.write(year+','+month+','+day+','+begin+','+end+','+obs1+','+Type+'\n')
                        fileOut.write(year+','+month+','+day+','+begin+','+end+','+obs2+','+Type+'\n')
                        fileOut.write(year+','+month+','+day+','+begin+','+end+','+col[20]+','+Type+'\n')
                    else:
                        for k in range(3,len(col)):
                            obs = col[k]
                            if "," in obs:
                                obs = obs.rstrip(obs[-1])
                            fileOut.write(year+','+month+','+day+','+begin+','+end+','+obs+','+Type+'\n')
                else:
                        for k in range(3,len(col)):
                            obs = col[k]
                            if "," in obs:
                                obs = obs.rstrip(obs[-1])
                            if "," in obs:
                                obs1 = obs.rsplit(",")[0]
                                obs2 = obs.rsplit(",")[1]
                                fileOut.write(year+','+month+','+day+','+begin+','+end+','+obs1+','+Type+'\n')
                                fileOut.write(year+','+month+','+day+','+begin+','+end+','+obs2+','+Type+'\n')
                            else:
                                fileOut.write(year+','+month+','+day+','+begin+','+end+','+obs+','+Type+'\n')
"""                   
                    
#Repetimos todo para el año 2022. (Mejorar)    
url = 'http://soleil.i4ds.ch/solarradio/data/BurstLists/2010-yyyy_Monstein/2022/'
L = listFD2(url) #todos los reports de 2022

for i in range(len(L)):
    myfile = L[i].rsplit('/', 1)[1]
    myurl = url + myfile
    urllib.request.urlretrieve(myurl,myfile) #Descarga los events reports
    fileIn = open(myfile)
    rows = fileIn.readlines()
    if not "No" in rows[8]:
        year = myfile[11:15]
        month = myfile[16:18] 
        for j in range(8,len(rows)):          
            try:
                col=rows[j].rsplit()
                if ((len(col)>1)) and not ("##" in col[1]) and not (col[0]=="()" or col[0]=="[]" or col[0]=="???" or col[1]=="." or col[0]=="CAU"):                
                    day = col[0][6:8]
                    if ("59.21" in col[1] or "18.21" in col[1]):
                        split = col[1].rsplit(".")
                    else:
                        split = col[1].rsplit("-")
                
                    if len(split)<2: #Literalmente esto solo pasa una vez. Es un error de Monstein :((((
                        if (col[0]=="20211218"):
                            split2 = col[1].rsplit(".")
                            begin = split2[0]
                            end = split2[1]
                        else:
                            split2 = col[1].rsplit(":",2)
                            begin = split2[0].rsplit(":")[0]+split2[0].rsplit(":")[1]
                            end = split2[1]+split2[2]
                    elif ("_" in split[1]):
                        begin = split[0].rsplit(":")[0]+split[0].rsplit(":")[1]
                        end = split[1].rsplit("_")[0]+split[1].rsplit("_")[1]
                    elif ("." in split[0]):
                        begin = split[0].rsplit(".")[0]+split[0].rsplit(".")[1]
                        end = split[1].rsplit(":")[0]+split[1].rsplit(":")[1]
                    elif ("." in split[1]):
                        begin = split[0].rsplit(":")[0]+split[0].rsplit(":")[1]
                        end = split[1].rsplit(".")[0]+split[1].rsplit(".")[1]    
                    else:
                        begin = split[0].rsplit(":")[0]+split[0].rsplit(":")[1]
                        end = split[1].rsplit(":")[0]+split[1].rsplit(":")[1]
                    
                    Type = col[2]
                    if begin == "1416":
                        a=1
                    for k in range(3,len(col)):
                        obs = col[k]
                        if ",G" in obs or ",I" in obs:
                            a=1
                        elif "," in obs:
                            obs = obs.rstrip(obs[-1])
                            fileOut.write(year+','+month+','+day+','+begin+','+end+','+obs+','+Type+'\n')
                        
                        else: 
                            fileOut.write(year+','+month+','+day+','+begin+','+end+','+obs+','+Type+'\n')
                        
            except:
                continue
fileOut.close()            
    

"""
if (len(col)>19 and day=="01" and month=="03" and year=="2021"):
    if ("," in col[19].rstrip(col[19][-1])):
        fileOut.write(year+','+month+','+day+','+begin+','+end+','+col[19].rsplit(",")[0]+','+Type+'\n')
        fileOut.write(year+','+month+','+day+','+begin+','+end+','+col[19].rsplit(",")[1]+','+Type+'\n')
    else:
        for k in range(3,len(col)):
            obs = col[k]
            if "," in obs:
                obs = obs.rstrip(obs[-1])
            fileOut.write(year+','+month+','+day+','+begin+','+end+','+obs+','+Type+'\n')
"""    