import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def extract_data(PATH):
    """
    [data, labels, filename, df] = extract_data(PATH)

    """
    name = PATH.split("/")[-1][:-4]
    df = pd.read_csv(PATH)
    
    data = {}
    for i in range(len(df.columns)-1):
        # labels[df.columns[i]] = df.iloc[0,i]
        data[df.columns[i]] = df.iloc[:,i].values

    return data, name, df

def values_by_index(data, index):
        col_name = list(data.keys())
        # print(col_name)
        return data[col_name[index]][1:].astype(float)

def labels_by_index(data, index):
        col_name = list(data.keys())

        return col_name[index], data[col_name[index]][0]

def interpolate1(time, data, tolerance = 0.3):
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

    return newtime, newdata


    # not a good approach!    
def interpolate2(time, data, step=50):
    newdata = np.array([data[0]])
    newtime = np.array([time[0]])
    for i in range(1,np.size(data),step):
        newdata = np.append(newdata, np.mean(data[i:i+step]))
        newtime = np.append(newtime, time[i])
         
    return newtime, newdata

def avg_diff(time, data, st = 2, tol = 0.005):
    # first avg then diff
    [new_time1, new_data1] = interpolate2(time, data, step = st)
    [new_time, new_data] = interpolate1(new_time1, new_data1, tolerance = tol)
                                    
    return new_time, new_data
    
#### Create Ramp ####
def create_ramp(time, data, csvname="", name="ramplines.txt", ramp_id="ramp_id", initial_tau=0, final_tau=10):
    fileloc = f"{csvname}/{name}"

    with open(fileloc, "w") as f:
        for i in range(initial_tau,final_tau):
            f.write(f"&RAMP ID='{ramp_id}', T={time[i]:.2f}, F={data[i]/np.max(data):.2f} /\n")

    f.close()

#### Post #####

def compare_data_size(data_original, data_modified):
    size_old = np.size(data_original)
    size_new = np.size(data_modified)
    print()
    print(f"size of original data set: {size_old}")
    print(f"size of modified data set: {size_new}")


def disp_plot(orgtime, orgdata, newtime, newdata, data, name): 
    # plt.clf()
    plt.scatter(orgtime,orgdata, label="real",s=1)
    plt.plot(newtime,newdata, "k*--", label="interpolated")
    
    plt.grid()
    [x_name, x_dim] = labels_by_index(data, 0)
    [y_name, y_dim] = labels_by_index(data, 1)
    plt.title(f"{name} | {np.size(newdata)} points")
    plt.xlabel(f"{x_name} {x_dim}")
    plt.ylabel(f"{y_name} {y_dim}")
    plt.tight_layout()
    plt.legend()


def save_plot(name):
    plt.savefig(name, dpi=500,facecolor='white', transparent=False)



def divide_data1(time, data, division_line, overlap):
    """
    [time1, tim2, heating_rate1, heating_rate2] = divide_data1(data, division_line, overlap)
    """
    # division_line = 2.5 ## 2.5 Sandia ## 3 NIST
    # overlap = 2

    div = np.max(np.where(time/60 <= division_line))
    data1 = data[:div+overlap]
    data2 = data[div-overlap:]

    time1 = time[:div+overlap]
    time2 = time[div-overlap:]

    return time1, time2, data1, data2


def division1(time, data, division_line, overlap):
    # print(division_line)
    num_divs = len(division_line)
    if division_line[0] == 0:
        divs = np.zeros(num_divs+1)
    else:
        divs = np.zeros(num_divs+2)
        for i in range(len(divs)-2):
            # print(np.max(np.where(time/60<=division_line[i])))
            divs[i+1] = np.max(np.where(time/60<=division_line[i]))
    
    num_divs = len(divs)
    divs[num_divs-1] = len(time)-1
    divs = divs.astype(int)
    # print(divs)
    
    parts = len(divs)-1
    time_d = {}
    data_d = {}
    for i in range(parts):
        left_end = 1
        right_end = 1
        if (i == 0):
            left_end = 0
        elif(i+1 == parts):
            right_end = 0
            
        overlap_left = overlap*left_end
        overlap_right= overlap*right_end
        time_d[i] = time[divs[i]-overlap_left:divs[i+1]+overlap_right]
        data_d[i] = data[divs[i]-overlap_left:divs[i+1]+overlap_right]
        
    return time_d, data_d

def combine_parts(time_d, data_d,division_line,overlap):
    new_time = np.array([])
    new_data = np.array([])
    if division_line[0] == 0:
        parts = 1
    else:
        parts = len(division_line) + 1

    for i in range(parts-1):
        left_end =1 
        right_end=1
        if i == 0:
            left_end = 0
        elif i+1 == parts:
            right_end = 0

        l_cut = overlap*left_end
        r_cut = overlap*right_end
        new_time = np.append(new_time, time_d[i][l_cut:-r_cut])
        new_data = np.append(new_data, data_d[i][l_cut:-r_cut])

    new_time = np.append(new_time, time_d[parts-1][overlap:])
    new_data = np.append(new_data, data_d[parts-1][overlap:])
    
    return new_time, new_data