# __author__ = 'Becky(Imotions) + Ansh( Neruoscape hs intern :) )'
#script without threshold as artifact detection will be done in kubios, version 2.0 with artifact detection will be coming soon!
import matplotlib
#%matplotlib qt ---- import this function for interactivity
#%matplotlib widget or notebook ----  import this funciton for interactivity - better quality but must only review one graph at a time
import numpy as np
import matplotlib.pyplot as plt
import time
from easygui import enterbox
from easygui import multenterbox

def GetIBIs(origPPG,name, Scene,NewFilePath):

    #### PROCESSING PARAMETERS AND INITIALIZATIONS

    Fs = 102.4  # sampling rate
    N = 25  # Number of points in moving window
    D = 15
    B = []
    adjPPG = []
    PPG = []
    N2 = int(Fs / 5)
    t = [0]  ## holds the time signal
    T = []   #holds the threshold value at each point in time
    #Global IBI
    IBI = []  #A list of the times between each detected peak
    timestoremove=[] #will hold the indices in the original time signal and PPG signal that are removed as artifacts
    ppgstoremove=[]
    LastCheck=0 # this is only needed if removing part of data with code #Use this when checking if we just skipped over a time period while calculating and IBI... if the peak is found outside the removed period but the last peak was inside(lastcheck=1) dont calc ibi

    
    #### BUILD THE ORIGINAL TIME SIGNAL AND PLOT ORIGINAL SIGNAL
    for i in range(0, len(origPPG) - 1):
        t.append(1.0 / Fs + t[i])
        # 1.0/Fs == 0.009 + previous number in t list

    ##### REMOVING THE BASELINE DRIFT 
    for i in range((N - 1) / 2 * D, len(origPPG) - (N - 1) / 2 * D): # range usually around (25, 38017) - Will not always be the same because origPPG changes with files 
        summation = 0
        for j in range(-(N - 1) / 2, (N - 1) / 2): # range usually (-12, 12)
            summation = summation + origPPG[i + j * D]
            #  (i + j * D) = iterating number through range + another iterating number through range * 25
        adjPPG.append(origPPG[i] - summation / N)
        # adjPPG appending origPPG # - another origPPG which is divided by 25

    #### REMOVE HIGH FREQUENCY NOISE

    for i in range((N2 - 1) / 2, len(adjPPG) - (N2 - 1) / 2):
        summation = 0
        for j in range(-(N2 - 1) / 2, (N2 - 1) / 2):
            summation = summation + adjPPG[i + j]
        PPG.append(summation / N)

    for i in range(0,(N-1)/2*D+(N-1)/2-3): #25 + 9
        t.remove(t[0])# remove the oldest and newest point
        t.remove(t[-1])
    
   # plt.plot(t,PPG)
   # plt.title('HF Flitlered & Baseline Drift Removed ' + name)
    #name is name of file
   # plt.show(block=False)
   # can get rid of above hashtags to graph, see HF filtered and baseline drift removed data

   
   
    numregions= 0 #enterbox('how many regions would you like to remove?') - this is if we were to do artifacts in this code
    # note the code for removing artifacts and removing parts of the data that are not clean has been removed from the script
    if numregions== 0:
        numregions=int(numregions)
        fieldvals=[]

    tstart = np.argmax(PPG[0:int(Fs)])  # find the highest point in the first 50 points--- tstart is the first peak, the baseline threshold for points while looking at data to artifact
    for i in range(0, len(t)-int(.5*Fs)): 
        # ignore T - only relevant when artifacting/doesnt matter!
        T.append(1000000)# ---- threshold no one can crash/change - therefore get all data points so artifact in kubios
    

    Vmax=[T[0]]
    # vmax, and T[0] is the highest point so far
    Peaktime=[0,t[tstart]] # Add PPG[tstart] as the first peak point in the file 
    #t[tstart] is the time stamp correlating to the highest peak - on one case it was 2.1835
    # peaktime is the peaks! (ie.... data collected)
    IBI.append(1)  # assume 1s as the first IBI 
    RefractP = .6  # minimum time period between peaks
    sr = -.6
    fr = -3 # S&D peak detection weights from Shimmer Equation
    NPWS = int(.5 * Fs)  # Next Peak Window Start (consider points at least 30 away when searching for next peak)
    NPWE = int(1.2* Fs)  # Next Peak Window  End(consider points from NPWS to NPWE when searching for next peak - in this range)
    Vp = [max(PPG[tstart+NPWS:tstart+NPWE])] # Next Predicted Peak (based on Max in 90 s window)
    TVp=[t[PPG[tstart + NPWS:tstart + NPWE].index(Vp[-1]) + tstart + NPWS]]  # time of next predicted peak
    

    
    for i in range(tstart, len(t)-int(.5*Fs)):  # range ex. (52, 37249)
        # Start looping through points from tstart to the end of the time signal - all points before tstart are baseline and not considered 
        if ((t[i] - Peaktime[-1]) > RefractP): # this is saying if the timestamp - the previous peak timestamp is greater than least time between peaks, then look at code
          # the Peaktime[-1] is always changing to reflect the most recent peak timestamp
                if (PPG[i]==max(PPG[i-40:i+40])):  # If it's a local maximum --- + or - 40 makes it so that the ibi is proper length
                # if ppg is a local maximum then..... (look below)
                    Vmax.append(PPG[i]) # append the local maximum into Vmax
                    Peaktime.append(t[i]) #-- append the timestamp for this local maximum, IBI point - use this to calculate IBI data
                    if IBICheck==0: # LastCheck==0 only relevant when manually removing artifacts, so doesn't matter now!
                        if LastCheck==0:# LastCheck==0 only relevant when manually removing artifacts, so doesn't matter now! - it is always 0!
                            IBI.append(Peaktime[-1] - Peaktime[-2])
                            # RefractP = .5 * (np.mean(IBI[-2:-1])) --- figure out what this does and reinput in the code if it creates more accurate data!
                        else:
                            LastCheck=0
    
                             
                    
                
                IBICheck=0
                    
    #if len(IBI) == len(Peaktime ) - 1 :
        #print('The IBI and corresponding timestamps line up') ------- to check if the IBI's and corresponding time stamps allign, not more IBI's than timestamps

    NewFile1= open(NewFilePath+Scene+name, 'w')
    
   
    for i in range(0, len(IBI)):
        NewFile1.write(str(IBI[i]))
        NewFile1.write("\n")
        
        
    NewFile1.close()
    return(IBI)
   # plt.show(block=True)
   # Peaktime.remove(0)
   # T.remove(T[-1])
   # plt.plot(t)
   # plt.plot(t, PPG, t[0:len(T)],T,'bd', Peaktime, Vmax, 'rs')
   # plt.title('PPG Signal with Peaks in Red, Threshold in Blue')
  #  plt.show()
  #  not showing graph with this code, if want to see it take of above hashtags!
    
  