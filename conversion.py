#! usr/bin/env python3
import csv

with open('logResults.txt', 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split("/") for line in stripped if line)
    with open('logResults.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(('Date/Time', 'Rain','Max Wind','Average WInd','Wind DIr', 'Predicted Depth'))
        writer.writerows(lines)