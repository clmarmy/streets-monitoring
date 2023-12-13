import logging
import logging.handlers
import os
import requests

from io import BytesIO
import zipfile
from datetime import date
from datetime import timedelta
import geopandas as gpd
import pandas as pd
import csv


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"
    #logger.info("Token not available!")
    #raise


if __name__ == "__main__":
    
    url = ['https://data.geo.admin.ch/ch.swisstopo.amtliches-strassenverzeichnis/amtliches-strassenverzeichnis/amtliches-strassenverzeichnis_2056.gdb.zip',
        'https://data.geo.admin.ch/ch.swisstopo.amtliches-strassenverzeichnis/amtliches-strassenverzeichnis/amtliches-strassenverzeichnis_2056.csv.zip'] # STAC

    DIR_IN = 'data'
    previous_date = str(date.today()-timedelta(days = 1))
    new_path = os.path.join(DIR_IN,str(date.today()))


    logger.info('Downloading data and preparing file...')

    if os.path.isdir(new_path):
        logger.info('Directory already exists')
    else:
        os.mkdir(new_path)

        for el in url:
            # Downloading the file by sending the request to the URL
            req = requests.get(el)
            logger.info('Downloading Completed')

            if ('gdb' in el.split('/')[-1]):
                open(os.path.join(DIR_IN,str(date.today()),'gdb.zip'), 'wb').write(req.content)
            else:
            # extracting the zip file contents
                zipfile_ob= zipfile.ZipFile(BytesIO(req.content))
                zipfile_ob.extractall(os.path.join(DIR_IN,str(date.today())))

    if os.path.isfile(os.path.join(DIR_IN,'recap.csv')):
        logger.info('Recap CSV file already exists')
    else:
        with open(os.path.join(DIR_IN,'recap.csv'), 'w', newline='') as file:
            my_header = ['previous_date', 'new_date', 'sum_ESID_diff','sum_LABEL_diff', 'sum_previous_ESID', 'sum_new_ESID']
            writer = csv.writer(file)
            writer.writerow(my_header) 


    logger.info('Merging name on street...')
    
    street_geom_0=gpd.read_file(os.path.join(DIR_IN,previous_date,'gdb.zip')+'!pure_str.gdb', layer="PURE_LIN")
    street_geom_0_dup = street_geom_0.loc[street_geom_0.duplicated()]
    street_geom_0 = street_geom_0.drop_duplicates('geometry')
    street_name_0=pd.read_csv(os.path.join(DIR_IN,previous_date,'pure_str.csv'),sep=';')
    street_geom_name_0 = street_geom_0.merge(street_name_0,on=['STR_ESID'])

    street_geom_1=gpd.read_file(os.path.join(DIR_IN,str(date.today()),'gdb.zip')+'!pure_str.gdb', layer="PURE_LIN")
    street_geom_1_dup = street_geom_1.loc[street_geom_1.duplicated()]
    street_geom_1 = street_geom_1.drop_duplicates('geometry')
    street_name_1=pd.read_csv(os.path.join(DIR_IN,str(date.today()),'pure_str.csv'), sep=';')
    street_geom_name_1 = street_geom_1.merge(street_name_1,on=['STR_ESID'])

        
    logger.info('Joining geometries...')
    
    street_0_1_merge = street_geom_name_0.merge(street_geom_name_1, how='outer', on=['geometry'])
    street_0_1_merge['ESID_diff'] = street_0_1_merge['STR_ESID_x']==street_0_1_merge['STR_ESID_y'] 
    street_0_1_merge['LABEL_diff'] = street_0_1_merge['STN_LABEL_x']==street_0_1_merge['STN_LABEL_y'] 
    
    previous = street_0_1_merge.loc[pd.isna(street_0_1_merge['STR_ESID_y'])]
    new = street_0_1_merge.loc[pd.isna(street_0_1_merge['STR_ESID_x'])]
    inner = street_0_1_merge.loc[pd.notna(street_0_1_merge['STR_ESID_x']) & pd.notna(street_0_1_merge['STR_ESID_y'])]
    
    csv_row = [previous_date, date.today(), sum(street_0_1_merge['ESID_diff']==False), sum(street_0_1_merge['LABEL_diff']==False), 
               sum(pd.isna(street_0_1_merge['STR_ESID_y'])), sum(pd.isna(street_0_1_merge['STR_ESID_x']))]


    logger.info('Writing file...')
    
    with open(os.path.join(DIR_IN,'recap.csv'), 'a') as file:
        writer = csv.writer(file)
        writer.writerow(csv_row)
    
    # street_geom_0_dup.to_file(os.path.join(DIR_IN,(previous_date+'_duplicate.gpkg')))
    street_geom_1_dup.to_file(os.path.join(DIR_IN,(str(date.today())+'_duplicate.gpkg')))
    # street_0_1_merge.to_file(os.path.join(DIR_IN,(previous_date+'_'+str(date.today())+'_outer.gpkg')))
    previous.to_file(os.path.join(DIR_IN,(previous_date+'_'+str(date.today())+'_previous.gpkg')))
    new.to_file(os.path.join(DIR_IN,(previous_date+'_'+str(date.today())+'_new.gpkg')))
    # inner.to_file(os.path.join(DIR_IN,(previous_date+'_'+str(date.today())+'_inner.gpkg')))
