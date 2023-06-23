from df_to_ramp import *

PATH1 = "https://raw.githubusercontent.com/MaCFP/matl-db/master/PMMA/Calibration_Data/Sandia/Sandia_TGA_Ar_50K_3.csv"
PATH2 = "https://raw.githubusercontent.com/MaCFP/matl-db/master/PMMA/Calibration_Data/NIST/NIST_TGA_N2_10K_2.csv"
PATH3 = "https://raw.githubusercontent.com/MaCFP/matl-db/master/PMMA/Calibration_Data/NIST/NIST_DSC_N2_10K_3.csv"
PATH4 = "https://raw.githubusercontent.com/MaCFP/matl-db/master/PMMA/Calibration_Data/NIST/NIST_DSC_N2_10K_4.csv"
PATH5 = "https://raw.githubusercontent.com/MaCFP/matl-db/master/PMMA/Calibration_Data/NIST/NIST_DSC_N2_10K_5.csv"

# Gather Data and Display head
[time, temp, mass, name, df] = url_to_arr(PATH1 ,head=1)

heating_rate = np.gradient(temp,time/60)

time = time - time[0]

# dividing line
div = np.max(np.where(time/60<2.5))
heating_rate1 = heating_rate[:div]
heating_rate2 = heating_rate[div:]

time1 = time[:div]
time2 = time[div:]

def compare_and_plot(time,new_time, data, new_data):
    [size_old, size_new] = compare_data_size(time, new_time)
    disp_plot(time, data, new_time, new_data, name=name, unit="Heating Rate (dTdt) [Ks^-1]", param_size=tolerance, save_fig=1, type=1)


## composite of both interpolating methods. Applying them with different tolerances between each division of the plot.

# composite1: first avg(int-2) then diff(int-1)
tolerance = 0.12
[new_time1, new_data1] = comp_avg_diff(time1, heating_rate1, name, st=2, tol=tolerance)
compare_and_plot(time1/60,new_time1/60, heating_rate1, new_data1)

# composite2: first avg(int-2) then diff(int-1)
tolerance = 0.29
[new_time2, new_data2] = comp_avg_diff(time2, heating_rate2, name, st=10, tol=tolerance)
compare_and_plot(time2/60,new_time2/60, heating_rate2, new_data2)



# combining all composites
time = np.concatenate((time1,time2))
heating_rate = np.concatenate((heating_rate1,heating_rate2))
new_time = np.concatenate((new_time1,new_time2))
new_data = np.concatenate((new_data1,new_data2))

compare_and_plot(time/60,new_time/60, heating_rate, new_data)


