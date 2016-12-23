# Weather-Underground-API

# Purpose
Script parses JSON returned by the Weather Underground API to extract full location, and minimum and maximum forecast temperature in Celsius for up to 10 days for any number of cities. 

# Input
Enter the number of days you want to forecast. Minimum is 1 day and maximum is 10 days (for the free version of the API). List the cities you want temperatures for in locs. Locations can be specified in the formats described under Standard Request URL Format: https://polish.wunderground.com/weather/api/d/docs?d=data/index

# Output
A csv file that contains the full location and the 5 minimum and maximum forecast temperatures, one line per city.
