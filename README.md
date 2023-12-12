# actions-test
Script to monitor addresses.

## Hardware requirements
No specific requirements. 

## Software Requirements
No specific requirements.

## Folder structure

```
├── .github                       # 
  └── workflows
      ├── actions.yml             #  
      └── actions_rm.yml          # 
├── data
   ├── YYYY-MM-DD
      ├── output files            #  
      ├── .gdb                    # 
      └── .csv                    # 
├──.gitignore                     # 
├── README.md                     # 
├── main.py                       # 
└── requirements.txt              # 
└── status.log                    # 
```

## Scripts and Procedure

This repo documents changes between the data downloaded yesterday and today from STAC (https://data.geo.admin.ch/ch.swisstopo.amtliches-strassenverzeichnis/amtliches-strassenverzeichnis/).
The script makes a join between the GDBs of the two dates. The join is based on the geometries, which must be strictly identical to be joined.
In the CSV, there is a summary of changes between two dates:
* previous_date: e.g. yesterday
* new_date: e.g. today
* sum_ESID_diff: number of ESIDs that differ
* sum_LABEL_diff: number of different address labels
* sum_previous_ESID: the number of geometries/routes/addresses that only exist in the GDB of the previous_date
* sum_new_ESID: the number of geometries/routes/addresses that only exist in the new_date GDB

Vector results in detail:
* duplicate.gpkg: indicates geometries duplicated in the original GDBs. Only one is kept per duplicate for further analysis.
* outer.gpkg: contains the join union, what is joined and what could not be joined
* inner.gpkg: contains the intersection of the join, which is joined only
* previous.gpkg: contains geometries/routes/addresses that exist only in the previous_date GDB
* new.gpkg: geometries/routes/addresses that only exist in the GDB of new_date




