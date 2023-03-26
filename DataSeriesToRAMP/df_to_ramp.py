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

def dfplot(PATH, show_plot=1):
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
    if show_plot:
        plt.show()

    plt.scatter(time,mass, s=0.1)
    plt.grid()
    plt.title(f"{name},Mass/Time")
    plt.xlabel("Time[s]")
    plt.ylabel("Mass[mg]")
    plt.savefig(f"{name},masstemp.png", dpi=500,facecolor='white', transparent=False)
    if show_plot:
        plt.show()
    
##
# todo: two more functions:
# 1  that returns an array of temperature values from the array of given the time data points provided.
def create_ramp(PATH, filename=None, ramp_id=None, initial_tau=0, final_tau=10):
    [time, temp, mass, df] = url_to_arr(PATH1)
    if filename == None:
        filename = "ramp_lines.txt"
    if ramp_id == None:
        ramp_id = "ramp_id"
    with open(filename, "w") as f:
        for i in range(initial_tau,final_tau):
            f.write(f"&RAMP ID='{ramp_id}', T={time[i]:.2f}, F={temp[i]/np.max(temp):.2f}\n")

    f.close()

# 2  interpolation? based on how many data points needed (resolution of the array, but as a different function)
##
def interpolate_data(PATH, tolerance = 0.3, show_plot=1):
    [time, temp, mass, df] = url_to_arr(PATH)

    newtemp = np.array([temp[0]])
    newtime = np.array([time[0]])
    diff1 = temp[1] - temp[0]
    for i in range(1,np.size(temp)-1):
        diff2 = temp[i+1] - temp[i]
        if abs(diff1 - diff2) > tolerance:
            newtemp = np.append(newtemp, temp[i])
            newtime = np.append(newtime, time[i])
            diff1 = temp[i] - temp[i+1]


    newtime = np.append(newtime, time[-1])
    newtemp = np.append(newtemp, temp[-1])
    if show_plot:
        plt.clf()
        plt.scatter(time,temp, label="real")
        plt.scatter(newtime,newtemp, marker="*", label="interpolated")
        plt.grid()
        plt.title("Comparing Real with Interpolated")
        plt.xlabel("Time[s]")
        plt.ylabel("Temp[K]")
        plt.legend()
        plt.savefig(f"modified.png", dpi=500,facecolor='white', transparent=False)
        plt.show()
    
    return new_time, new_temp

    
if (__name__ == "__main__"):
    PATH1 = "https://raw.githubusercontent.com/MaCFP/matl-db/master/PMMA/Calibration_Data/NIST/NIST_DSC_N2_10K_5.csv"
    [time, temp, mass, df] = url_to_arr(PATH1,head=1)
    dfplot(PATH1,show_plot=0)
    interpolate_data(PATH1, tolerance = 0.3, show_plot=1)

