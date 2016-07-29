#!/bin/bash

python update_calendar2.py -i ~/volvo-journal-log.csv >html/charts/data/calendar2.csv
python update_progress.py -i ~/volvo-journal-log.csv >html/charts/data/progress.csv
python update_calendar.py -i ~/volvo-journal-log.csv >html/charts/data/distance.csv
python update_maintenance.py -i ~/volvo-journal-log.csv >html/charts/data/maintenance.csv

