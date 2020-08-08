#This script is for looping through the iMotions sensor data folder and calls to the IBI function which returns a list of IBIs. The variance of the IBI list is printed.
import os
import matplotlib
#%matplotlib notebook - interactive version of graph
#%matplotlib widget - interactive version of graph 
#%matplotlib qt - interactive version of graph
from matplotlib import pyplot as plt
#from ipywidgets import interact - if using the matplotlib widget  
import time
import numpy as np
from easygui import multenterbox

## CHANGE THE FOLDER TO THE FILE PATH OF THE IMOTIONS SENSOR DATA
# note the differences in file names for windows, mac, and linux operating systems while putting file names
# directory of the HRV data, script made to assess one section of data at a time (ex. MIST Pre, Mist FU, Mist Post all separately)
Folder='C:\Users\Ansh Verma\Desktop\MTYA_iMotions\MTYA_iMotionsPRE\Baseline_FU_ARTIFACTS'
# note, to make it save it in the proper folder, give the name of the beginning of the every file you would like to save after the folder you are going to save it in 
# with the Folder example above, Baseline_FU_ARTIFACTS/IBI_DATA_FOLDER - file name is last!
#fields=['SensorDataFolder','IBIDataFolder']
#Response=multenterbox('Enter the filepaths of your sensor data containing PPG signal and location to place IBI data files (note both pathways must exist ,and at the end of the pathway your putting the IBI data to put the name of the filename)', 'File Paths', fields)
#Response_1 = enterbox("please enter the file path where you would like to store the HRV data text files (note this pathway must exist ,and at the end of the pathway put the name of the filename) ")
#Folder=  Response[0]
#NewFilePath= Response[1]
#HRV_Pathway =  Response_1[0]
NewFilePath = 'C:\Users\Ansh Verma\Desktop\MTYA_iMotions\MTYA_iMotionsPRE\Test_Folder\IBI'
HRV_Pathway = 'C:\Users\Ansh Verma\Desktop\MTYA_iMotions\MTYA_iMotionsPRE\Test_Folder\HRV_Data'




## LOOP THROUGH FILES
#print(Folder)
HRV_list = []

for root, dirs, filenames in os.walk(Folder):

    for file in filenames:
        
        #print(file) - if you would like to see files

        respondent=file[:-4]
        openfile=open(Folder+"\\"+file,"r")
        c=0

        Stimuli=['Fixation'] # stimuli to recognize assessing the proper file, no need to change because MIST and Baseline file Stimuli already accounted for in following code
        # if there is a error mistake for the stimuli, most likely due human error during data collection, add accounting that stimuli in indicated code below
        RawPPG=[]  #holds the full Raw PPG signal column
        HRVs=[]
        stimscol=[]  #holds the full Stimulus name
        RawInd=[]    #temporarily holds the indices of the rows with PPG data for each scene
        firstrow=1

        for line in openfile:  ##Loop through this file and populate stimuli column and PPG column
            row=line.split("\t") # rows are collumns!
            v = 0
            check = 0
            while v <= 26:
                 # data collumn is 'Internal ADC A13 CAL (mVolts) (Shimmer Sensor)'), this while loop finds the data collumn
                if bool(row[v] == 'Internal ADC A13 CAL (mVolts) (Shimmer Sensor)') == True or bool(row[v] == 'Internal ADC A13 CAL (mVolts) (Shimmer)') == True:
                    x = v
                    #print(x) # printing x for all files allows you to see what the common rows for the PPG data is, and which ones are different due to human error
                    break
                else:
                    v = v + 1
                    continue
            while check <= 10: #does the same thing as the while loop above, but for the stimuli collumn!
                if bool(row[check] == 'StimulusName') == True or bool(row[check].lower == 'stimulusname') == True or bool(row[check].upper == 'STIMULUSNAME') == True or bool(row[check].upper == 'STIMULUS') == True:
                    check_1 = check
                    print(check_1)
                    break
                else:
                    check = check + 1
                    continue
            if check_1 < 3:
                check_1 = 5 # this is the normal index of the stimulus row
                    
            if firstrow==1: # skips the collumn description namename in the collumns 
                firstrow=0
            else:
                RawPPG.append(float(row[x]))
                stimscol.append(row[check_1]) # stiumli row has been constant thus far, it might change in some files due to human error, so watch out for this!
        for Scene in Stimuli:
            for i in range (0,len(stimscol)-1): #determine what the indices are for this scene
                # checking if the stimscol, file stimuli corresponds or is equal to our input stimuli
                # below if statement accounts for other common error names/MIST file names (other than the original Scene variable name earlier in this script)
                if stimscol[i][0:10]==Scene[0:10] or stimscol[i][0:10]==Scene[0:10].upper() or stimscol[i][0:10]=='MIST Task'or 'MIST' or 'mist' :
                    RawInd.append(i)
                    # appends the amount of stimuli in the file (indexes for them) 

            start=min(RawInd) #start/end points in RawPPG to send for IBIs
            end=max(RawInd)
            # rawppg is orig ppg
            #name is file name
            #scene is stimuli name
            #newfilepath is where writing it to as a file(the end of file path you put) 
            IBIs=GetIBIs(RawPPG[start:end],file, Scene, NewFilePath) 
            #print(IBIs) # prints IBI markers that go into the text file  - none in there
        sum=0
        for i in range(0,len(IBIs)-2):
            #print(len(IBIs)) - to see length of IBIs
            sum=sum+(IBIs[i+1]-IBIs[i])**2
            # hrv is heart rate variablility in general!
            HRV=(1.0/(len(IBIs)-1))*np.sqrt(sum) # IF there is only 1 IBI, then it will not work
        HRV_list.append(HRV)# HRV data for the dat set
        
    list1 = []   
    for file in filenames: # appends files to a list to call back upon later
        list1.append(file)
        
        
NewFile= open(HRV_Pathway, 'w')
for i in range(0, len(HRV_list) ):
    NewFile.write(list1[i]) # prints the list that corresponds to the HRV
    NewFile.write(str(' '))
    NewFile.write(str('='))
    NewFile.write(str(' '))
    NewFile.write(str(HRV_list[i]))
    NewFile.write("\n")
        
        
NewFile.close()
    
    
    
    
    
    
    
    
    
    
    
            
 