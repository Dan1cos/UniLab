# Project Alarms
A project for predicting air raid alarms
(everything could be done by performing each script step by step, how it's written in here(files with * can be skipped))

# Project execution

To run creation of the model run script ""

To run creation of the current alarms run script "makingFileEachHour"

To run creation of the endpoint run "SaaS_alarms"

# Files

## Model creation

### isw_download

File for downloading data from the ISW site from 24.02.22 to 25.01.23

### SelectHtmlBody

First part of preprocessing. Selecting main body from the html pages of ISW

### RemovingUnnecessaryData

Main part of preprocessing. Removing useless info and making text out of html

### Vectorize

Vectorizing data received from the previous part of preprocessing for further fitting ML model 

### WeatherScript

Script for getting weather for the selected place. Can be used with date to get info for 24 hours and without date to get info about next 12 hours

### ConvertingVectorToDF_EDA.py

Script for creating dataframe with all words and adding weights of that words for each day(correlation matrix was also calculated here to make some EDA)

### MergingData

Merging all data from previous sources(weather, alarms, words, cities) to one dataframe

### SplittingTrainTest

Splitting merged data into train and test data(also converting some string and datetime typed into floats)

### TrainingModel

Editing data so it would be possible to fit the model, training and testing model

### FeatureEngineering*

Script for getting number of alarms of the day and number of alarms in the regions on specific time

### save_page*

Script for returning selected page

---

## Current alarms creation

### ISWPrediction

Getting info about specific date and converting it into the dataframe with previous words

### CollectForecast

Collecting forecast for the specific date for all regions and editing it for further fitting into the model

### makingFileEachHour

Script for predicting alarms for next 12 hours and saving results in file 

---

## Endpoint creation

### SaaS_alarms

Endpoint for getting info out of file with all alarms
