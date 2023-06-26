''' 
Using interpolation methods (but with more customizability) to minimize the number of points over a given data set.
Interpolations used:
    - First order differences (with user provided tolerance)
    - Average of a given range of points (with user provided range)
    
What is done:
    1) The plot is divided based on the shape, so interpolation methods are applied with different tolerance values.
    2) two-step interpolation: Average is applied first, then Differences.
'''
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
division_line = 2.5 ## 2.5 Sandia ## 3 NIST
overlap = 2

div = np.max(np.where(time/60<division_line))
heating_rate1 = heating_rate[:div+overlap]
heating_rate2 = heating_rate[div-overlap:]

time1 = time[:div+overlap]
time2 = time[div-overlap:]

def compare_and_plot(time,new_time, data, new_data, show=False):
    new_name = name
    [size_old, size_new] = compare_data_size(time, new_time)
    disp_plot(time, data, new_time, new_data, name=new_name, unit="Heating Rate (dTdt) [Ks^-1]", param_size=tolerance, save_fig=1, type=1, show=show)


## composite of both interpolating methods. Applying them with different tolerances between each division of the plot.

# composite1: first avg(int-2) then diff(int-1)
tolerance = 0.15 ## 0.01 NIST ## 0.12 Sandia TGA
[new_time1, new_data1] = comp_avg_diff(time1, heating_rate1, name, st=2, tol=tolerance)
compare_and_plot(time1/60,new_time1/60, heating_rate1, new_data1)

# composite2: first avg(int-2) then diff(int-1)
tolerance = 0.29 ## 0.25 NIST ## 0.29 Sandia TGA
[new_time2, new_data2] = comp_avg_diff(time2, heating_rate2, name, st=10, tol=tolerance)
compare_and_plot(time2/60,new_time2/60, heating_rate2, new_data2)



# combining all composites
time = np.concatenate((time1[:-overlap],time2[overlap:]))
heating_rate = np.concatenate((heating_rate1[:-overlap],heating_rate2[overlap:]))
new_time = np.concatenate((new_time1[:-overlap],new_time2[overlap:]))
new_data = np.concatenate((new_data1[:-overlap],new_data2[overlap:]))

compare_and_plot(time/60,new_time/60, heating_rate, new_data, show=True)

create_ramp(time, new_data, filename="Sandia_TGA_RAMP.txt", 
            ramp_id="T_RAMP", initial_tau=0, final_tau=len(new_data))


