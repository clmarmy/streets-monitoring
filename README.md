# actions-test
This GitHub repo documents changes between the yesterday and today streets and adresses downloaded from official STAC repo: https://data.geo.admin.ch/ch.swisstopo.amtliches-strassenverzeichnis/amtliches-strassenverzeichnis/.

## Hardware requirements
No specific requirements. 

## Software Requirements
No specific requirements.

## Folder structure

```
├── .github                       # actions directory
  └── workflows
      ├── actions.yml             # action downloading and processing the data
      └── actions_rm.yml          # action deleting old downlaoded data folders
├── data
   ├── YYYY-MM-DD                 # data folders
      ├── .gdb                    # GDB with geometries and ESID
      └── .csv                    # CSV with data attributes                     
  └── *output files               # output files after processing
├── main.py                       # processing scripts run during GitHub action
├── requirements.txt              # libraries used by GitHub action to build the python environnement 
└── status.log                    # Stauts log from runs
```

## Scripts and Procedure
The script makes a join between the GDBs of yesterday and today. The join is based on the geometries, which must be strictly identical to be joined.
In the CSV, there is a summary of changes between the two dates:
* previous_date: yesterday
* new_date: today
* sum_ESID_diff: number of ESIDs that differ
* sum_LABEL_diff: number of different adress labels
* sum_previous_ESID: the number of geometries/streets/adresses that only exist in the previous_date GDB
* sum_new_ESID: the number of geometries/streets/adresses that only exist in the new_date GDB

Vector results in data folder:
* YYYY-MM-DD_duplicate.gpkg: geometries duplicated in the original GDBs. Only one geometry per duplicate is kept for further analysis.
* YYYY-MM-DD_YYYY-MM-DD_previous.gpkg: geometries/streets/adresses that exist only in the previous_date GDB.
* YYYY-MM-DD_YYYY-MM-DD_new.gpkg: geometries/streets/addresses that only exist in the new_date GDB.




