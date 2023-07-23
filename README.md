
# SmallFireThings

Collection of small(-ish) scripts that might be interesting for others and have no place to stay (yet). Maybe also for collecting ideas that can be spun off into their own packages in the future.

  

## DataSeries_to_RAMP

The main purpose of this program is to
- approximate the .csv files with experimental data
- the approximation should be able to recreate the experimental data with 'few' data points
- the data points are then used to create RAMP lines to be used in FDS input file.

  

### Approximation

The approximation is done using two methods

1) The data is averaged to 'smooth' out the points and prevent jaggedness in the data. The user can select the `step` size i.e. range of values to average.

2) The difference between the corresponding values at i and i+1 is calculated, and based on a user-defined `tolerance` value, it is decided whether the index should be ignored or not.

  

### Dividing the Dataset

- The two methods can be applied on the entire dataset or the user can also divide up the dataset using `division_lines`.

- Now each part of the data set can be approximated using different `step` and `tolerance` values.

- Additionally, the user can also choose how many points can overlap between each part using `overlap`

## Instructions
### User Inputs

`PATH`: location of the dataset
`division_line`:  takes in the time (in seconds) as the location where the data is divided
`overlap` : number of points shared between each divided part
`tolerance` : how much difference to be accepted between data[i] and data[i+1] (different value for each divided part)
`step`: range of points to be taken for averaging (different value for each divided part)
`plotname` = suffix of the generated plot
Below is an example of how the inputs are used:

Below are examples of how these inputs are used for different cases:
#### For multiple divisions:
`PATH` = "DataSets/Sandia_TGA_Ar_50K_3.csv"
`division_line` = [138.0,480.0]
`overlap` = 2
`tolerance` = [0.15,0.33,0.29]
`step` = [3,22,20]
`plotname` = f"{len(division_line)}div"

#### For no (or zero) divisions:
`PATH` = "DataSets/Sandia_TGA_Ar_50K_3.csv"
`division_line` = [0]
`tolerance` = [0.05]
`step` = [30]
`plotname` =  "0div"
