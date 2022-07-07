# gpu-price-tracker
Small project to keep track of current gpu price developments by checking prices and availability on (potentially multiple) websites.

NOTE: This project is not meant to force high workload on the respective websites but to keep track of price / availability developments over longer time periods. 

Currently the tracker is only designed to work with the proshop.dk website.

# How to run
In order to run this small bot, you want to run the python main.py file.
Running it at given time intervals to keep track of prices can be done with the 
help of schedulers such as cron (for linux).

NOTE: Ensure to set paths for cron working directories correctly to store the json file correctly as path is not stored absolute. 
> Sample cron job: 0 12 * * * cd [PATH-TO-RESULTFOLDER] && /usr/bin/python [PATH-TO-PROJECTFOLDER]/main.py >> [PATH-TO-CRONLOGFOLDER]/cron.log 2>&1

Before running the script you should change the config_sample.py to config.py
and insert all the relevant information in the config.

