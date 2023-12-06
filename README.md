# 3110-differential-privacy-final-project
This repo is for the final project for CS3110 - differential privacy. A linking attack will (hopefully) be conducted.

There is a csv from kaggle (https://www.kaggle.com/datasets/sumaiaparveenshupti/los-angeles-crime-data-20102020) that has all reported crime in los angeles from 2010-present with features including date occured, location, weapon, and description of the crime. There is an auxilary dataset (https://www.cdcr.ca.gov/capital-punishment/condemned-inmate-list-secure-request/) that is scraped using BeautifulSoup, with features including condemned inmate name, age, offense data...

The goal is to be able to link both of these datasets to be able to release pieces of related data from each dataset including the inmates name, the description of the crime they commited, and the weapon used.
