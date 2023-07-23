from funcs_1 import *
from directory_func import *

# USER INPUT

PATH = "DataSets/Sandia_TGA_Ar_50K_3.csv" 

division_line = [138,480]             # float divison location (seconds) # 2.3, 8 in minutes
overlap = 2                                     # int overlap size (indices on each end) # 2
tolerance = [0.15,0.33,0.29]         # float (size= len(division_line)+1) # 0.15, 0.33, 0.29
step = [3,22,20]                          # int (size= len(division_line)+1) # 3, 22, 20
plotname = f"{len(division_line)}div"           # plotname

## For no divisions ## 
# division_line = [0]             # float divison location (seconds) # 2.3, 8
# tolerance = [0.05]      # float (size= len(division_line)+1) # 0.15, 0.33, 0.29
# step = [30]                    # int (size= len(division_line)+1) # 3, 22,
# plotname = "0div"


################################################
if division_line[0] == 0: 
    overlap = 0 

division_line = np.array(division_line)/60

[data, csvname, df] = extract_data(PATH)
# make a separate directory for results with name f"{csvname}"
make_results_dir(csvname)


time = values_by_index(data, 0)
temp = values_by_index(data, 1)

heating_rate = np.gradient(temp,time/60)
time = (time - time[0])


[time_d, data_d] = division1(time, heating_rate, division_line, overlap=overlap) 

new_time_d = {}
new_data_d = {}
if len(time_d) > 1:
    for i in range(len(division_line)+1):
        [new_time_d[i], new_data_d[i]] = avg_diff(time_d[i], data_d[i], st=step[i], tol=tolerance[i])
        disp_plot(time_d[i], data_d[i], new_time_d[i], new_data_d[i], data, name=f"{csvname}")
        plt.show()
        compare_data_size(time_d[i], new_time_d[i])    

else:
    i = 0
    [new_time_d[i], new_data_d[i]] = avg_diff(time_d[i], data_d[i], st=step[i], tol=tolerance[i])
    # disp_plot(time_d[i], data_d[i], new_time_d[i], new_data_d[i], data, name=f"{csvname}")
    # plt.show()
    compare_data_size(time_d[i], new_time_d[i])    

print("\n::Combining Part(s)::")
[new_time, new_data] = combine_parts(new_time_d, new_data_d,division_line,overlap)
plt.clf()
disp_plot(time, heating_rate, new_time, new_data, data, name=f"{csvname}")
compare_data_size(time, new_time)
if division_line[0] != 0:
    for i in range(len(division_line)):
        plt.plot(np.ones(2)*division_line[i]*60,[0,np.max(heating_rate)],"--", color="#d0312d")
save_plot(f"{csvname}/{csvname}_{plotname}")
plt.show()


# create ramp file
create_ramp(new_time, new_data, csvname, name=f"ramplines_{plotname}.txt", initial_tau=0, final_tau=len(new_data))

print("inputlog")
f = open(f"{csvname}/inputlog_{csvname}.txt","a")
f.write(f"""
# path                  :: {PATH}
# plotname              :: {plotname}    
# division_lines        :: {division_line} 
# overlap_size          :: {overlap}          
# tolerance(s)          :: {tolerance}         
# avg_range_sizes(s)    :: {step}              
""")
f.close()