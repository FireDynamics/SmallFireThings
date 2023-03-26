from df_to_ramp import *

PATH1 = "https://raw.githubusercontent.com/MaCFP/matl-db/master/PMMA/Calibration_Data/NIST/NIST_TGA_N2_10K_1.csv"
PATH2 = "https://raw.githubusercontent.com/MaCFP/matl-db/master/PMMA/Calibration_Data/NIST/NIST_TGA_N2_10K_2.csv"
PATH3 = "https://raw.githubusercontent.com/MaCFP/matl-db/master/PMMA/Calibration_Data/NIST/NIST_DSC_N2_10K_3.csv"
PATH4 = "https://raw.githubusercontent.com/MaCFP/matl-db/master/PMMA/Calibration_Data/NIST/NIST_DSC_N2_10K_4.csv"
PATH5 = "https://raw.githubusercontent.com/MaCFP/matl-db/master/PMMA/Calibration_Data/NIST/NIST_DSC_N2_10K_5.csv"


[time, temp, mass, name, df] = url_to_arr(PATH4 ,head=1)
dfplot(time, temp, mass, name,show_plot=1, save_fig=0)

#tolerance parameter might have to be tweaked
# for mass
[new_time, new_data] = interpolate1(time, mass, name, unit="Mass[kg]", tolerance = 0.01, show_plot=1)

#for temp
#[new_time, new_data] = interpolate_data(time, temp, name, unit="Temp[K]", tolerance = 0.01, show_plot=1)

[size_old, size_new] = compare_data_size(time, new_time)
create_ramp(time, new_data, filename="ramp_lines.txt", initial_tau=0, final_tau=size_new)