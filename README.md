# [DEPRICATED] RKI Inzidenz History for chosen German disctricts and cities

NOTE: DOES NOT WORK ANYMORE

Running the python script will download the newest XLSX file from RKI and extract the relevant data. Which then in turn will be put into a generated static HTML page

This will be ran by a cronjob on a RasPI every hour and the resulting HTML will be put into index.html and pushed to the GitHub repo.

The static site is reachable here: https://eversojoe.github.io/rki-inzidenz-history/
