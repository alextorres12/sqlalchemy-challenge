# SQL Alchemy Challenge
Northwestern University Data Science Boot Camp

[Homework 10](https://nu.bootcampcontent.com/NU-Coding-Bootcamp/nu-chi-data-pt-08-2020-u-c/tree/master/02-Homework/10-Advanced-Data-Storage-and-Retrieval/Instructions)

## Climate Analysis and Exploration
In this project, I used Jupyter Notebook and a pre-existing SQLite database to do basic climate analysis and data exploration of the database. First, I utilized the datetime library to query the last 12 months of precipitation data then plot the precipitation against the date with matplotlib. 

Then, I ran a few queries that found the number of observations at each weather station, the station with the highest number of observations, and created a histogram of temperature readings at the most popular station.

## Climate App
In this section of the project, I designed and built a Flask API to perform the following functions at different endpoints. All data was returned in JSON format:

- Homepage to list all of the routes
- Precipitation endpoint to return the last year of preciptation data
- Stations endpoint to return a complete list of stations including: station code, name, lat, long, and elevation
- Temperature endpoint to return the last year of temperature readings
- Date endpoints to return the min, max, and avg temperatures in a date range or after a start date
