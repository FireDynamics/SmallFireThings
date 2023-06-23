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
    name = disp_csv_name(PATH)
    
    return time, temp, mass, name, df

def disp_csv_name(PATH):
    name = re.search("[^\/]+$", PATH).group()[:-4]
    return name

def dfplot(time, temp, mass, name, show_plot=1, save_fig=1):
    plt.clf()
    plt.scatter(time,temp, s=0.1)
    plt.grid()
    plt.title(f"{name},Temperature/Time")
    plt.xlabel("Time[s]")
    plt.ylabel("Temperature[k]")
    plt.savefig(f"{name},timetemp.png", dpi=500,facecolor='white', transparent=False)
    if show_plot:
        plt.show()

    plt.clf()
    plt.scatter(time,mass, s=0.1)
    plt.grid()
    plt.title(f"{name},Mass/Time")
    plt.xlabel("Time[s]")
    plt.ylabel("Mass[mg]")
    if save_fig:
        plt.savefig(f"{name},masstemp.png", dpi=500,facecolor='white', transparent=False)
    if show_plot:
        plt.show()
    

def create_ramp(time, data, filename=None, ramp_id=None, initial_tau=0, final_tau=10):
    if filename == None:
        filename = "ramp_lines.txt"
    if ramp_id == None:
        ramp_id = "ramp_id"
    with open(filename, "w") as f:
        for i in range(initial_tau,final_tau):
            f.write(f"&RAMP ID='{ramp_id}', T={time[i]:.2f}, F={data[i]/np.max(data):.2f}\n")

    f.close()

#### INTERPOLATION ########

# select the values that differ greatly from the previous data point
def interpolate1(time, data, name, unit="Temp[K]", tolerance = 0.3, show_plot=0, save_fig=1):
    newdata = np.array([data[0]])
    newtime = np.array([time[0]])
    diff1 = data[1] - data[0]
    for i in range(1,np.size(data)-1):
        diff2 = data[i+1] - data[i]
        if abs(diff1 - diff2) > tolerance:
            newdata = np.append(newdata, data[i])
            newtime = np.append(newtime, time[i])
            diff1 = data[i+1] - data[i]


    newtime = np.append(newtime, time[-1])
    newdata = np.append(newdata, data[-1])
    
    if show_plot:
        disp_plot(time, data, newtime, newdata, name, unit, tolerance, save_fig, type=1)
    return newtime, newdata

# not a good approach!    
def interpolate2(time, data, name, unit="Temp[K]", step=50, show_plot=0, save_fig=1):
    newdata = np.array([data[0]])
    newtime = np.array([time[0]])
    for i in range(1,np.size(data),step):
        newdata = np.append(newdata, np.mean(data[i:i+step]))
        newtime = np.append(newtime, time[i])
    
    if show_plot:
        disp_plot(time, data, newtime, newdata, name, unit, step, save_fig, type=2)
    
    return newtime, newdata

 
def disp_plot(time, data, newtime, newdata, name, unit, param_size, save_fig, type):
    plt.clf()
    plt.scatter(time,data, label="real",s=1)
    plt.plot(newtime,newdata, "k*--", label="interpolated")
    plt.grid()
    if (type == 1):
        param = "tol"
    elif (type == 2):
        param = "rng"
    plt.title(f"Comparing {name} with Interpolation-{type} [{param}:{param_size}] with {np.size(newdata)} points")
    plt.xlabel("Time[min]")
    plt.ylabel(unit)
    plt.tight_layout()
    plt.legend()
    if save_fig:
        plt.savefig(f"interpolated{type}_{unit}_{name}.png", dpi=500,facecolor='white', transparent=False)
    plt.show()
 
   
def compare_data_size(data_original, data_modified):
    size_old = np.size(data_original)
    size_new = np.size(data_modified)
    print()
    print(f"size of original data set: {size_old}")
    print(f"size of modified data set: {size_new}")
    
    return size_old, size_new

### COMPOSITES ###
def comp_avg_diff(time, mass, name, st = 3, tol = 0.005, show_plot=0):
    # first interpolate2 (avg) then interpolate1 (diff)
    [new_time1, new_data1] = interpolate2(time, mass, name, unit="Mass[kg]",                                    step = st, show_plot=0)
    [new_time, new_data] = interpolate1(new_time1, new_data1, name, unit="Mass[kg]", tolerance = tol,show_plot=show_plot)
                                    
    return new_time, new_data
    
def comp_diff_avg(time, mass, name, st = 3, tol = 0.005, show_plot=0):
    # first interpolate1 (diff) then interpolate2 (avg)
    [new_time1, new_data1] = interpolate2(time, mass, name, unit="Mass[kg]",step = st, show_plot=0)
    [new_time, new_data] = interpolate1(new_time1, new_data1, name, unit="Mass[kg]", tolerance = tol, show_plot=show_plot)

    
if (__name__ == "__main__"):
    PATH1 = "https://raw.githubusercontent.com/MaCFP/matl-db/master/PMMA/Calibration_Data/NIST/NIST_DSC_N2_10K_3.csv"
    [time, temp, mass, name, df] = url_to_arr(PATH1 ,head=1)
    dfplot(time, temp, mass, name,show_plot=0)
    
    [new_time1, new_data1] = interpolate1(time, mass, name, unit="Mass[kg]", tolerance = 0.005, show_plot=1)
    [new_time2, new_data2] = interpolate2(time, mass, name, unit="Mass[kg]", step = 10, show_plot=1)
    
    [size_old, size_new1] = compare_data_size(time, new_time1)
    [size_old, size_new2] = compare_data_size(time, new_time2)
    
    create_ramp(time, new_data1, filename="ramp_lines1.txt", initial_tau=0, final_tau=size_new1)
