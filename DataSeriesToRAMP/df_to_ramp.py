import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re


def url_to_arr(PATH, head=0):
    # PATH, head=0 {df.head()}
    df = pd.read_csv(PATH)
    if head:
        print(f"\ndata set for: {disp_csv_name(PATH)}")
        print(df.head())
    time = df.iloc[1:,0].values.astype("float")
    temp = df.iloc[1:,1].values.astype("float")
    mass = df.iloc[1:,2].values.astype("float")
    
    return time, temp, mass, df

def disp_csv_name(PATH):
    name = re.search("[^\/]+$", PATH).group()[:-4]
    return name

def dfplot(PATH, show=1):
    # PATH, show=1 {plt.show()}
    name = disp_csv_name(PATH)
    [time, temp, mass, df] = url_to_arr(PATH)
    # print(name)
    plt.scatter(time,temp, s=0.1)
    plt.grid()
    plt.title(f"{name},Temperature/Time")
    plt.xlabel("Time[s]")
    plt.ylabel("Temperature[k]")
    plt.savefig(f"{name},timetemp.png", dpi=500,facecolor='white', transparent=False)
    if show:
        plt.show()

    plt.scatter(time,mass, s=0.1)
    plt.grid()
    plt.title(f"{name},Mass/Time")
    plt.xlabel("Time[s]")
    plt.ylabel("Mass[mg]")
    plt.savefig(f"{name},masstemp.png", dpi=500,facecolor='white', transparent=False)
    if show:
        plt.show()
    
##
# two functions:
# 1  that returns an array of temperature values from the array of given the time data points provided.
# 2  interpolation? based on how many data points needed (resolution of the array, but as a different function)
## 
    
if (__name__ == "__main__"):
    PATH1 = "https://raw.githubusercontent.com/MaCFP/matl-db/master/PMMA/Calibration_Data/NIST/NIST_DSC_N2_10K_5.csv"
    [time, temp, mass, df] = url_to_arr(PATH1,head=1)
    dfplot(PATH1,show=0)