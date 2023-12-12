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
      └── actions_rm.yml          # action deleting old downloads
├── data
   ├── YYYY-MM-DD                 # data folder
      ├── output files            # output files after processing
      ├── .gdb                    # GDB with geometries and ESID
      └── .csv                    # CSV with data attributes                     # 
├── main.py                       # processing scripts run during GitHub action
└── requirements.txt              # library used by GitHub action to build the python environnement 
└── status.log                    # Stauts log from runs
```

## Scripts and Procedure
The script makes a join between the GDBs of the two dates. The join is based on the geometries, which must be strictly identical to be joined.
In the CSV, there is a summary of changes between the two dates:
* previous_date: yesterday
* new_date: today
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




