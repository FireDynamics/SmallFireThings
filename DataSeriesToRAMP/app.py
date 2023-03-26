from df_to_ramp import *

PATH1 = "https://raw.githubusercontent.com/MaCFP/matl-db/master/PMMA/Calibration_Data/NIST/NIST_DSC_N2_10K_5.csv"
[time, temp, mass, df] = url_to_arr(PATH1,1)
dfplot(PATH1,show=0)

filename = "output.txt"
f = open(filename,'w')
with open(filename) as file:
    for i in range(10):
        f.write(f"line: {i}\n")
        
# f.write(f"\n\n !VENT SURFS!\n\n")
f.write("\n")
f.close()
print(i)