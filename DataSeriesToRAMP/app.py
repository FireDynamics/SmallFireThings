from df_to_ramp import *


PATH1 = "https://raw.githubusercontent.com/MaCFP/matl-db/master/PMMA/Calibration_Data/NIST/NIST_DSC_N2_10K_5.csv"
[time, temp, mass, df] = url_to_arr(PATH1,1)
dfplot(PATH1,show=0)