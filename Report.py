import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import warnings 
import numpy as np
from datetime import datetime
warnings.filterwarnings('ignore')

#AUX FUNCTION----------------------------------------------------------------------------------
def sum_hour(hour,minute):
    hora = hour[0:2]
    minuto = hour[2:4]
    segundo = hour[4:6]
    hora1 = dt.timedelta(hours = int(hora), minutes = int(minuto), seconds = int(segundo))
    hora_suma = dt.timedelta(minutes=int(minute))
    suma = hora1+hora_suma
    
    #Si segundo es >=30 se añade un minuto
    #BUENA IDEA ??????????????????????????????????????????
    if (int(segundo)>=30):
        suma = suma + dt.timedelta(minutes=1)
    #---------------------------------------------------
    
    split = str(suma).rsplit(":")
    new_minuto=split[1]
    if (len(split[0])<=1):
        new_hora = "0"+split[0]
    else:
        new_hora = split[0]
        
    resultado = new_hora + new_minuto
    return resultado

def round_hour(hour):
    segundo = hour[4:6]
    time = datetime.strptime(hour, "%H%M%S")

    #Si segundo es >=30 se añade un minuto. BUENA IDEA ?????
    if (int(segundo)>=30): time = time + dt.timedelta(minutes=1)
    #---------------------------------------------------
    
    time = str(time)
    new_time = time[11:13]+time[14:16]
    return new_time

#---------------------------------------------------------------------------------------------

  
def obtain_predictions_NEW(txt): #txt is the name of the txt file (so you should add .txt)
    path='C:/Users/Usuario/Desktop/e-Callisto/NeuralNetwork/Predictions/'
    file = open(path+txt)
    rows = file.readlines()
    prediction_list = []
    for i in range(len(rows)):
        if (not len(rows[i])<=1):
            day = rows[i].rsplit()[1].rsplit("_")[3]
            hour = rows[i].rsplit()[1].rsplit("_")[4]
            hour = round_hour(hour)
            if (("SI" in rows[i].rsplit()[3]) or ("ASSAerupcion" in rows[i].rsplit()[3])):
                prediction=True
            else:
                prediction=False

            triplex = [day,hour,prediction]
            prediction_list.append(triplex)
    return prediction_list

def obtain_predictions_threshold(txt,th): #txt is the name of the txt file (so you should add .txt)
    path='C:/Users/Usuario/Desktop/e-Callisto/NeuralNetwork/Predictions/'
    file = open(path+txt)
    rows = file.readlines()
    prediction_list = []
    for i in range(len(rows)):
        cols = rows[i].rsplit()
        if (not len(rows[i])<=1):
            day = cols[1].rsplit("_")[3]
            hour = cols[1].rsplit("_")[4]
            hour = round_hour(hour)
            if th <= 50:                
                if (("SI" in cols[3]) or ("ASSAerupcion" in cols[3]) or (float(cols[4][0:len(cols[4])-1])<=(100-th))):
                    prediction=True
                else:
                    prediction=False
            else:
                tr_check = float(cols[4][0:len(cols[4])-1])
                if ("SI" in cols[3]) and (tr_check>=th):
                    prediction=True
                else:
                    prediction=False

            triplex = [day,hour,prediction]
            prediction_list.append(triplex)
    return prediction_list


def obtain_predictions_csv(csv):
    path='C:/Users/Usuario/Desktop/e-Callisto/Predictions_ScriptDIGITS/'
    predictions = pd.read_csv(path+csv, encoding= 'unicode_escape')
    predictions = predictions.dropna()
    prediction_list = []
    for i in range(len(predictions)):
        file = predictions.filename[i].rsplit("_")
        day = file[len(file)-3]
        hour = file[len(file)-2]
        hour = round_hour(hour)   
        if "1" in str(predictions.pred[i]):
            prediction=True
        else:
            prediction=False
        triplex = [day,hour,prediction]
        prediction_list.append(triplex)
        
        """
        if i%15 == 0:
            run = cols[1].rsplit("/")[3].rsplit(".")[0] + ".fit.gz"
        fourplet = [day,hour,prediction, run]
        prediction_list.append(fourplet)
        """
    return prediction_list


def obtain_predictions_csv_th(csv,th):
    path='C:/Users/Usuario/Desktop/e-Callisto/Predictions_ScriptDIGITS/'
    predictions = pd.read_csv(path+csv, encoding= 'unicode_escape')
    predictions = predictions.dropna()
    prediction_list = []
    for i in range(len(predictions)):
        file = predictions.filename[i].rsplit("_")
        day = file[len(file)-3]
        hour = file[len(file)-2]
        hour = round_hour(hour)   
        if (predictions.pred_1[i] >= th):
            prediction=True
        else:
            prediction=False
        triplex = [day,hour,prediction]
        prediction_list.append(triplex)
        
        
        """
        if i%15 == 0:
            run = cols[1].rsplit("/")[3].rsplit(".")[0] + ".fit.gz"
        fourplet = [day,hour,prediction, run]
        prediction_list.append(fourplet)
        """
    return prediction_list

def coincidences(date, begin, end, noaa): #for coincidences with NOAA or CALLISTO report
    noaa2=noaa
    #noaa2[['Year', 'Month','Day']] = noaa2[['Year', 'Month','Day']].astype(str)
    noaa2 = noaa2.loc[(noaa['Year']==int(date[0:4]))] #Select year
    noaa2 = noaa2.loc[(noaa2['Month']==int(date[4:6]))] #Select month
    noaa2 = noaa2.loc[(noaa2['Day']==int(date[6:8]))] #Select day
    
    case1 = noaa2.loc[(noaa2['Begin']>=begin)]
    case1 = case1.loc[(case1['Begin']<=end)]
    case1 = case1.loc[(case1['End']>end)]
    
    case2 = noaa2.loc[(noaa2['End']>=begin)]
    case2 = case2.loc[(case2['End']<=end)]
    case2 = case2.loc[(case2['Begin']<begin)]
    
    case3 = noaa2.loc[(noaa2['Begin']<begin)]
    case3 = case3.loc[(case3['End']>end)]
    
    case4 = noaa2.loc[(noaa2['Begin']>=begin)]
    case4 = case4.loc[(case4['Begin']<=end)]
    case4 = case4.loc[(case4['End']<=end)]
    
    time_list=[]
    coincidence=False
    if len(case1)>=1:
        coincidence=True
        for i in case1.index:
            time=case1['Begin'][i][0:2]+':'+case1['Begin'][i][2:4]+'-'+case1['End'][i][0:2]+':'+case1['End'][i][2:4]
            time_list.append(time)
    if len(case2)>=1:
        coincidence=True
        for i in case2.index:
            time=case2['Begin'][i][0:2]+':'+case2['Begin'][i][2:4]+'-'+case2['End'][i][0:2]+':'+case2['End'][i][2:4]
            time_list.append(time)
    if len(case3)>=1:
        coincidence=True
        for i in case3.index:
            time=case3['Begin'][i][0:2]+':'+case3['Begin'][i][2:4]+'-'+case3['End'][i][0:2]+':'+case3['End'][i][2:4]
            time_list.append(time)
    if len(case4)>=1:
        coincidence=True
        for i in case4.index:
            time=case4['Begin'][i][0:2]+':'+case4['Begin'][i][2:4]+'-'+case4['End'][i][0:2]+':'+case4['End'][i][2:4]
            time_list.append(time)
               
    return[coincidence,time_list]

def cross_pred(date, begin, end, predictions2): #for report_crossmatch
    #Añadir +-1 minutos????
    pd2 = pd.DataFrame(predictions2)
    pd_true = pd2[2]==np.bool_(True)
    pd2=pd2[pd_true]
    
    pd2 = pd2.loc[pd2[0]==date]
    pd2 = pd2.loc[pd2[1]>=sum_hour(begin+"00",-1)]
    pd2 = pd2.loc[pd2[1]<=sum_hour(end+"00",1)]

    if len(pd2)>=1:
        return True
    else:
        return False
#-----------------------------------------------------------------------------------------------------






#REPORT FUNCTIONS-------------------------------------------------------------------------------------
def report(txt): #Cross validation with NOAA
    path = 'C:/Users/Usuario/Desktop/e-Callisto/Report_Creation/'
    file_name = txt[0:len(txt)-4]+"_Report.txt"
    file = open(path + file_name, "w")
    file.write("# " + txt.rsplit(".")[0] + '\n\n' + "#Date \t\tTime \t\tIn_NOAA\n#-------------------------------------------------\n")
    
    #predictions = obtain_predictions_OLD(txt)
    #predictions = obtain_predictions_NEW(txt)
    predictions = obtain_predictions_csv(txt)
    
    path_noaa='C:/Users/Usuario/Desktop/e-Callisto/NOAA/NOAAEvents.csv'  
    noaa = pd.read_csv(path_noaa, encoding= 'unicode_escape')
    
    if (predictions[0][2]==True):
        date=predictions[0][0]
        begin=predictions[0][1]
        iterator = 1
        end=begin
        while (predictions[iterator][2]==True and iterator < len(predictions)):
            end=predictions[iterator][1]
            iterator=iterator+1
        
        time = begin[0:2]+":"+begin[2:4]+"-"+end[0:2]+":"+end[2:4]
        in_noaa = coincidences(date, begin, end, noaa)
        if in_noaa[0]==False:
            file.write(date+"\t" + time + '\n')
        else:
            for i in range(len(in_noaa[1])):
                file.write(date+"\t" + time + "\tYes("+ in_noaa[1][i] +')\n')
    
    
    for i in range(1,len(predictions)):
        if (predictions[i][2]==True and predictions[i-1][2]==False):
            date=predictions[i][0]
            begin=predictions[i][1]
            iterator = i+1
            end=begin
            while (predictions[iterator][2]==True and iterator < len(predictions)):
                end=predictions[iterator][1]
                iterator=iterator+1
            
            time = begin[0:2]+":"+begin[2:4]+"-"+end[0:2]+":"+end[2:4]
            in_noaa = coincidences(date, begin, end, noaa)
            if in_noaa[0]==False:
                file.write(date+"\t" + time + '\n')
            else:
                times = ""
                for j in range(len(in_noaa[1])):
                    times = times + in_noaa[1][j]+","
                times = times[0:(len(times)-1)]
                file.write(date+"\t" + time + "\tYes["+ times +']\n')    

    file.close()
    
    
def report_callisto(txt): #Cross validation with othe e-Callisto stations and NOAA
    path = 'C:/Users/Usuario/Desktop/e-Callisto/Report_Creation/'
    file_name = txt[0:len(txt)-4]+"_Report_Callisto.txt"
    file = open(path + file_name, "w")
    file.write("# " + txt.rsplit(".")[0] + '\n\n' + "#Date \t\tTime \t\tIn_NOAA \t\t\t\tIn_Callisto\n#--------------------------------------------------------------------------------------------\n")
    
    predictions = obtain_predictions_NEW(txt)
    
    path_noaa='C:/Users/Usuario/Desktop/e-Callisto/NOAA/NOAAEvents.csv'  
    noaa = pd.read_csv(path_noaa, encoding= 'unicode_escape')
    path_callisto='C:/Users/Usuario/Desktop/e-Callisto/CallistoReports/CallistoEventsNoObs.csv'  
    callisto = pd.read_csv(path_callisto, encoding= 'unicode_escape')
    
    if (predictions[0][2]==True):
        date=predictions[0][0]
        begin=predictions[0][1]
        iterator = 1
        end=begin
        while (predictions[iterator][2]==True and iterator < len(predictions)):
            end=predictions[iterator][1]
            iterator=iterator+1
        
        time = begin[0:2]+":"+begin[2:4]+"-"+end[0:2]+":"+end[2:4]
        in_noaa = coincidences(date, begin, end, noaa)
        in_callisto = coincidences(date, begin, end, callisto)
        if in_noaa[0]==False and in_callisto[0]==False:
            file.write(date+"\t" + time + '\n')
        elif in_noaa[0]==True and in_callisto[0]==False:
            times = ""
            for j in range(len(in_noaa[1])):
                times = times + in_noaa[1][j]+","
            times = times[0:(len(times)-1)]
            file.write(date+"\t" + time + "\tYes["+ times +']\n')
        elif in_noaa[0]==False and in_callisto[0]==True:
            times = ""
            for j in range(len(in_callisto[1])):
                times = times + in_callisto[1][j]+","
            times = times[0:(len(times)-1)]
            file.write(date+"\t" + time + "\tYes["+ times +']\n')
        else:
            times_noaa = ""
            times_callisto = ""
            for j in range(len(in_noaa[1])):
                times_noaa = times_noaa + in_noaa[1][j]+","
            times_noaa = times_noaa[0:(len(times)-1)]
            for j in range(len(in_callisto[1])):
                times_callisto = times_callisto + in_callisto[1][j]+","
            times_callisto = times_callisto[0:(len(times)-1)]
            file.write(date+"\t" + time + "\tYes["+ times_noaa +']' + "\tYes["+ times_callisto +']\n')
            
    for i in range(1,len(predictions)):
        if (predictions[i][2]==True and predictions[i-1][2]==False):
            date=predictions[i][0]
            begin=predictions[i][1]
            iterator = i+1
            end=begin
            while (predictions[iterator][2]==True and iterator < len(predictions)):
                end=predictions[iterator][1]
                iterator=iterator+1
            
            time = begin[0:2]+":"+begin[2:4]+"-"+end[0:2]+":"+end[2:4]
            in_noaa = coincidences(date, begin, end, noaa)
            in_callisto = coincidences(date, begin, end, callisto)
            if in_noaa[0]==False and in_callisto[0]==False:
                file.write(date+"\t" + time + '\t------\t\t\t\t\t-------\n')
            elif in_noaa[0]==True and in_callisto[0]==False:
                times = ""
                for j in range(len(in_noaa[1])):
                    times = times + in_noaa[1][j]+","
                times = times[0:(len(times)-1)]
                file.write(date+"\t" + time + "\tYes["+ times +']\t\t\t------\n')
            elif in_noaa[0]==False and in_callisto[0]==True:
                times = ""
                for j in range(len(in_callisto[1])):
                    times = times + in_callisto[1][j]+","
                times = times[0:(len(times)-1)]
                file.write(date+"\t" + time + "\t------\t\t\t\t\tYes["+ times +']\n')
            else:
                times_noaa = ""
                times_callisto = ""
                for j in range(len(in_noaa[1])):
                    times_noaa = times_noaa + in_noaa[1][j]+","
                times_noaa = times_noaa[0:(len(times_noaa)-1)]
                for k in range(len(in_callisto[1])):
                    times_callisto = times_callisto + in_callisto[1][k]+","
                times_callisto = times_callisto[0:(len(times_callisto)-1)]
                file.write(date+"\t" + time + "\tYes["+ times_noaa +']' + "\t\t\tYes["+ times_callisto +']\n')
   

    file.close()    
    
    
def report_crossmatch(txt1,txt2): #Cross validation with other prediction file and NOAA
    #En el futuro hay que hacerlo para una lista de txt
    path = 'C:/Users/Usuario/Desktop/e-Callisto/Report_Creation/'
    file_name = txt1[0:len(txt1)-4]+"_Report.txt"
    file = open(path + file_name, "w")
    file.write("# " + txt1.rsplit(".")[0] + '\n\n' + "#Date \t\tTime \t\tCross-match \tIn_NOAA\n#-------------------------------------------------------------------------------------------------\n")
    
    predictions1 = obtain_predictions_csv(txt1)
    predictions2 = obtain_predictions_csv(txt2)
    
    path_noaa='C:/Users/Usuario/Desktop/e-Callisto/NOAA/NOAAEvents.csv'  
    noaa = pd.read_csv(path_noaa, encoding= 'unicode_escape')
    
    if (predictions1[0][2]==True):
        date=predictions1[0][0]
        begin=predictions1[0][1]
        iterator = 1
        end=begin
        while (predictions1[iterator][2]==True and iterator < len(predictions1)):
            end=predictions1[iterator][1]
            iterator=iterator+1
        
        time = begin[0:2]+":"+begin[2:4]+"-"+end[0:2]+":"+end[2:4]
        in_noaa = coincidences(date, begin, end, noaa)
        cross = cross_pred(date,begin,end,predictions2)
        if in_noaa[0]==False and cross==False:
            file.write(date+"\t" + time + '\t------\t\t\t\t\t-------\n')
        elif in_noaa[0]==True and cross==False:
            times = ""
            for j in range(len(in_noaa[1])):
                times = times + in_noaa[1][j]+","
            times = times[0:(len(times)-1)]
            file.write(date+"\t" + time + "\tYes["+ times +']\t\t\t------\n')
        elif in_noaa[0]==False and cross==True:
            file.write(date+"\t" + time + "\t------\t\t\t\t\tYes\n")
        else:
            times = ""
            for j in range(len(in_noaa[1])):
                times = times + in_noaa[1][j]+","
            times = times[0:(len(times)-1)]
            file.write(date+"\t" + time + "\tYes["+ times +']\t\t\tYes\n')
            
    for i in range(1,len(predictions1)):
        if (predictions1[i][2]==True and predictions1[i-1][2]==False):
            date=predictions1[i][0]
            begin=predictions1[i][1]
            iterator = i+1
            end=begin
            while (predictions1[iterator][2]==True and iterator < len(predictions1)):
                end=predictions1[iterator][1]
                iterator=iterator+1
        
            time = begin[0:2]+":"+begin[2:4]+"-"+end[0:2]+":"+end[2:4]
            in_noaa = coincidences(date, begin, end, noaa)
            cross = cross_pred(date,begin,end,predictions2)
            
            if in_noaa[0]==False and cross==False:
                file.write(date+"\t" + time + '\t-------\t\t-------\n')
            elif in_noaa[0]==True and cross==False:
                times = ""
                for j in range(len(in_noaa[1])):
                    times = times + in_noaa[1][j]+","
                times = times[0:(len(times)-1)]
                file.write(date+"\t" + time + '\t-------\t\tYes['+ times+']\n')
            elif in_noaa[0]==False and cross==True:
                file.write(date+"\t" + time + "\tYes\t\t-------\n")
            else:
                times = ""
                for j in range(len(in_noaa[1])):
                    times = times + in_noaa[1][j]+","
                times = times[0:(len(times)-1)]
                file.write(date+"\t" + time + "\tYes" + "\t\tYes["+ times +']\n')
    file.close() 
#-----------------------------------------------------------------------------------------------


#In_Progress
def obtain_matrix(csv_list):
    path='C:/Users/Usuario/Desktop/e-Callisto/Predictions_ScriptDIGITS/'

    #stations = ["BIR","GLASGOW","HUMAIN","ROSWELL-NM","RWANDA",]
    #En el futuro, poner mejores nombres a los csv para poder obtener el nombre de las estaciones de ellos.
    
    predictions = pd.read_csv(path+csv_list[0], encoding= 'unicode_escape')
    predictions = predictions.dropna()
    file_begin = predictions.filename[0].rsplit("_")
    day_begin = file_begin[len(file_begin)-3]
    file_end = predictions.filename[len(predictions.filename)-1].rsplit("_")
    day_end = file_end[len(file_end)-3]
    days_lapse = int(day_end)-int(day_begin)+1
    
    
    m = np.zeros(((len(csv_list)), 1440*days_lapse), dtype = bool) #Revisar numero columnas
    
    
    for i in range(len(csv_list)):
        predictions = obtain_predictions_csv(csv_list[i])
        predictions = pd.DataFrame(predictions)
        pd_true = predictions[2]==np.bool_(True)
        predictions=predictions[pd_true]
        for j in predictions.index:
            minute = int(str(predictions[1][j])[2:4])
            hour = int(str(predictions[1][j])[0:2])
            day = int(str(predictions[0][j])[6:8])
            
            index=1440*(day-1) + 60*hour + minute
            
            m[i,index]=True

    return m


def obtain_matrix_NOAA(csv_list): #NOTA: los intervalos grandes se comen a los intervalos cortos así que se pierde esa información...
    path_noaa = 'C:/Users/Usuario/Desktop/e-Callisto/NOAA/NOAAEvents.csv' 
    
    path='C:/Users/Usuario/Desktop/e-Callisto/Predictions_ScriptDIGITS/'

    #stations = ["BIR","GLASGOW","HUMAIN","ROSWELL-NM","RWANDA",]
    #En el futuro, poner mejores nombres a los csv para poder obtener el nombre de las estaciones de ellos.
    
    predictions = pd.read_csv(path+csv_list[0], encoding= 'unicode_escape')
    predictions = predictions.dropna()
    file_begin = predictions.filename[0].rsplit("_")
    day_begin = file_begin[len(file_begin)-3]
    file_end = predictions.filename[len(predictions.filename)-1].rsplit("_")
    day_end = file_end[len(file_end)-3]
    days_lapse = int(day_end)-int(day_begin)+1
    
    noaa = pd.read_csv(path_noaa, encoding= 'unicode_escape')
    
    noaa2=noaa
    #noaa2[['Year', 'Month','Day']] = noaa2[['Year', 'Month','Day']].astype(str)
    noaa2 = noaa2.loc[(noaa['Year']>=int(day_begin[0:4]))] #Select >= year
    noaa2 = noaa2.loc[(noaa2['Month']>=int(day_begin[4:6]))] #Select >= month
    noaa2 = noaa2.loc[(noaa2['Day']>=int(day_begin[6:8]))] #Select >= day
    
    noaa2 = noaa2.loc[(noaa['Year']<=int(day_end[0:4]))] #Select <= year
    noaa2 = noaa2.loc[(noaa2['Month']<=int(day_end[4:6]))] #Select <= month
    noaa2 = noaa2.loc[(noaa2['Day']<=int(day_end[6:8]))] #Select <= day
    
    m = np.zeros(((len(csv_list)+1), 1440*days_lapse), dtype = bool) #Revisar numero columnas
    
    
    for i in noaa2.index:
        day = noaa2['Day'][i]
        begin = noaa2['Begin'][i]
        end = noaa2['End'][i]
        
        iterator = begin
        while int(iterator) <= int(end):
            hour = int(str(iterator)[0:2])
            minute = int(str(iterator)[2:4])
            
            index = 1440*(day-1) + 60*hour + minute
            m[0,index]=True
            
            
            iterator = str(int(iterator) + 1)
            if len(iterator)<=3:
                iterator = '0'+iterator
                if len(iterator)<=3:
                    iterator = '0'+iterator
                    if len(iterator)<=3:
                        iterator = '0'+iterator
            if str(iterator)[2]=='6':
                iterator = str(int(iterator) + 40) #-60+100
                if len(iterator)<=3:
                    iterator = '0'+iterator
            
    
    for i in range(len(csv_list)):
        predictions = obtain_predictions_csv(csv_list[i])
        predictions = pd.DataFrame(predictions)
        pd_true = predictions[2]==np.bool_(True)
        predictions=predictions[pd_true]
        for j in predictions.index:
            minute = int(str(predictions[1][j])[2:4])
            hour = int(str(predictions[1][j])[0:2])
            day = int(str(predictions[0][j])[6:8])
            
            index=1440*(day-1) + 60*hour + minute
            
            m[i,index]=True

    return m


#El objetivo será intentar quitar argumentos. O no, no sé jajaj
#También: meter funciones auxiliares para aligerar el código.
def report_matrix(matrix, name_month, year, month, stations_names): #Por ahora name_month = CELESTINA_YYYY_mm.txt
    path = 'C:/Users/Usuario/Desktop/e-Callisto/Report_Creation/'
    file = open(path + name_month+".txt", "w")
    file.write("# Product: " + name_month + '\n# Prepared by CELESTINA\n\n' + "#Date \t\tTime \t\tStations\n#-------------------------------------------------------------------------------------------------\n")

    for j in range(matrix.shape[1]):
        column = matrix[1:,j]
        pdcolumn = pd.DataFrame(column)
        pdcolumn_true = pdcolumn.loc[(pdcolumn[0]==True)]
        if len(pdcolumn_true) > 0:
            stations_list = ""
            for i in pdcolumn_true.index:
                stations_list = stations_list + stations_names[i]+", "

            stations_list = stations_list[0:(len(stations_list)-2)]
            day = 1 + j//1440
            if day<10:
                day = "0" + str(day)
            else:
                day = str(day)
            date = year+month+day
            
            rest_day = j%1440
            hour = rest_day//60
            minute = rest_day%60
            
            if hour<10:
                hour = "0" + str(hour)
            else:
                hour = str(hour)
                
            if minute<10:
                minute = "0" + str(minute)
            else:
                minute = str(minute)
                
            time = hour+minute
            
            
            file.write(date+"\t" + time + '\t' + stations_list +'\n')
    file.close() 

#MAIN-------------------------------------------------------------------------------------------
#th=0.05
    

#txt = "AGL_GLA_2014_02.txt"   
#txt = "Landschlacht_2021_11.txt"

csv1 = "results_BIR2014_07.csv"
#csv2 = "results_BIR2014_07.csv"
csv2 = "results_GLASGOW2014_07.csv"


#report_crossmatch(csv1,csv2)
#report(csv1)

#report(txt)
#report_callisto(txt)
    
    
    
csv_list = ["results_bir201411.csv", "results_glasgow201411.csv", "results_humain201411.csv", "results_roswell201411.csv", "results_rwanda201411.csv"]
stations_names = ["BIR", "GLASGOW", "HUMAIN", "ROSWELL", "RWANDA"]
year = "2014"
month = "11"
m = obtain_matrix_NOAA(csv_list)


#plt.imshow(m[:,:500])
report_matrix(m, "November", year, month, stations_names)

"""
pbir = obtain_predictions_csv(csv_list[0])
pbir = pd.DataFrame(pbir)
pd_true = pbir[2]==np.bool_(True)
pbir=pbir[pd_true]

pgla = obtain_predictions_csv(csv_list[1])
pgla = pd.DataFrame(pgla)
pd_true = pgla[2]==np.bool_(True)
pgla=pgla[pd_true]

phum = obtain_predictions_csv(csv_list[2])
phum = pd.DataFrame(phum)
pd_true = phum[2]==np.bool_(True)
phum=phum[pd_true]

pros = obtain_predictions_csv(csv_list[3])
pros = pd.DataFrame(pros)
pd_true = pros[2]==np.bool_(True)
pros=pros[pd_true]

prwa = obtain_predictions_csv(csv_list[4])
prwa = pd.DataFrame(prwa)
pd_true = prwa[2]==np.bool_(True)
prwa=prwa[pd_true]

m = obtain_matrix(csv_list)
"""
    
    




    

#------------------------------------------------------------------------------------------------
"""
def report_callisto(txt): #Cross validation with other e-Callisto stations and NOAA
    path = 'C:/Users/Usuario/Desktop/e-Callisto/Report_Creation/'
    file_name = txt[0:len(txt)-4]+"_Report_Callisto.txt"
    file = open(path + file_name, "w")
    file.write("# " + txt.rsplit(".")[0] + '\n\n' + "#Date \t\tTime \t\tIn_NOAA \t\t\t\tIn_Callisto\n#--------------------------------------------------------------------------------------------\n")
    heading = ["#Date","Time","In_NOAA", "In-Callisto"]
    line = f"{heading[0]:<10}{heading[1]:<10}{heading[2]:<10}{heading[3]:<30}"
    predictions = obtain_predictions_NEW(txt)
    
    path_noaa='C:/Users/Usuario/Desktop/e-Callisto/NOAA/NOAAEvents.csv'  
    noaa = pd.read_csv(path_noaa, encoding= 'unicode_escape')
    path_callisto='C:/Users/Usuario/Desktop/e-Callisto/CallistoReports/CallistoEventsNoObs.csv'  
    callisto = pd.read_csv(path_callisto, encoding= 'unicode_escape')
    
    if (predictions[0][2]==True):
        date=predictions[0][0]
        begin=predictions[0][1]
        iterator = 1
        end=begin
        while (predictions[iterator][2]==True and iterator < len(predictions)):
            end=predictions[iterator][1]
            iterator=iterator+1
        
        time = begin[0:2]+":"+begin[2:4]+"-"+end[0:2]+":"+end[2:4]
        in_noaa = coincidences(date, begin, end, noaa)
        in_callisto = coincidences(date, begin, end, callisto)
        if in_noaa[0]==False and in_callisto[0]==False:
            file.write(date+"\t" + time + '\n')
        elif in_noaa[0]==True and in_callisto[0]==False:
            times = ""
            for j in range(len(in_noaa[1])):
                times = times + in_noaa[1][j]+","
            times = times[0:(len(times)-1)]
            file.write(date+"\t" + time + "\tYes["+ times +']\n')
        elif in_noaa[0]==False and in_callisto[0]==True:
            times = ""
            for j in range(len(in_callisto[1])):
                times = times + in_callisto[1][j]+","
            times = times[0:(len(times)-1)]
            file.write(date+"\t" + time + "\tYes["+ times +']\n')
        else:
            times_noaa = ""
            times_callisto = ""
            for j in range(len(in_noaa[1])):
                times_noaa = times_noaa + in_noaa[1][j]+","
            times_noaa = times_noaa[0:(len(times)-1)]
            for j in range(len(in_callisto[1])):
                times_callisto = times_callisto + in_callisto[1][j]+","
            times_callisto = times_callisto[0:(len(times)-1)]
            file.write(date+"\t" + time + "\tYes["+ times_noaa +']' + "\tYes["+ times_callisto +']\n')
            
    for i in range(1,len(predictions)):
        if (predictions[i][2]==True and predictions[i-1][2]==False):
            date=predictions[i][0]
            begin=predictions[i][1]
            iterator = i+1
            end=begin
            while (predictions[iterator][2]==True and iterator < len(predictions)):
                end=predictions[iterator][1]
                iterator=iterator+1
            
            time = begin[0:2]+":"+begin[2:4]+"-"+end[0:2]+":"+end[2:4]
            in_noaa = coincidences(date, begin, end, noaa)
            in_callisto = coincidences(date, begin, end, callisto)
            if in_noaa[0]==False and in_callisto[0]==False:
                file.write(date+"\t" + time + '\t------\t\t\t\t\t-------\n')
            elif in_noaa[0]==True and in_callisto[0]==False:
                times = ""
                for j in range(len(in_noaa[1])):
                    times = times + in_noaa[1][j]+","
                times = times[0:(len(times)-1)]
                info = f"columna1 {times:<20} hola"
                
                file.write(date+"\t" + time + "\tYes["+ times +']\t\t\t------\n')
            elif in_noaa[0]==False and in_callisto[0]==True:
                times = ""
                for j in range(len(in_callisto[1])):
                    times = times + in_callisto[1][j]+","
                times = times[0:(len(times)-1)]
                file.write(date+"\t" + time + "\t------\t\t\t\t\tYes["+ times +']\n')
            else:
                times_noaa = ""
                times_callisto = ""
                for j in range(len(in_noaa[1])):
                    times_noaa = times_noaa + in_noaa[1][j]+","
                times_noaa = times_noaa[0:(len(times_noaa)-1)]
                for k in range(len(in_callisto[1])):
                    times_callisto = times_callisto + in_callisto[1][k]+","
                times_callisto = times_callisto[0:(len(times_callisto)-1)]
                file.write(date+"\t" + time + "\tYes["+ times_noaa +']' + "\t\t\tYes["+ times_callisto +']\n')
   

    file.close()    
"""
    