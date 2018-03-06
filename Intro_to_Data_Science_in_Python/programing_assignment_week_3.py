# Assignment 3 - More Pandas
# This assignment requires more individual learning then the last one did - you are encouraged to check out the pandas documentation to find functions or methods you might not have used yet, or ask questions on Stack Overflow and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.


# Question 1 (20%)
# Load the energy data from the file Energy Indicators.xls, which is a list of indicators of energy supply and renewable electricity production from the United Nations for the year 2013, and should be put into a DataFrame with the variable name of energy.

# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:

# ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']

# Convert Energy Supply to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as np.NaN values.

# Rename the following list of countries (for use in later questions):

# "Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"

# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these,

# e.g.

# 'Bolivia (Plurinational State of)' should be 'Bolivia',

# 'Switzerland17' should be 'Switzerland'.



# Next, load the GDP data from the file world_bank.csv, which is a csv containing countries' GDP from 1960 to 2015 from World Bank. Call this DataFrame GDP.

# Make sure to skip the header, and rename the following list of countries:

# "Korea, Rep.": "South Korea",
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"



# Finally, load the Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology from the file scimagojr-3.xlsx, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame ScimEn.

# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15).

# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015'].

# This function should return a DataFrame with 20 columns and 15 entries.

import pandas as pd
import numpy as np

def answer_one():

    eng_ind_import_df = pd.read_excel('Energy Indicators.xls', skiprows=17, skip_footer=38, names=['nuller', 'nuller2', 'Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'])
    energy = eng_ind_import_df.drop(['nuller', 'nuller2'], axis=1).replace('...',np.nan)
    energy['Energy Supply'] = energy['Energy Supply'] * 1000000
    energy['Country'] = energy['Country'].str.replace('\d+', '')
    energy['Country'] = energy['Country'].str.replace(r"\(.*\)","")

    energy.loc[energy['Country']=='Republic of Korea','Country',] = 'South Korea'
    energy.loc[energy['Country']=='Iran ','Country',] = 'Iran'
    energy.loc[energy['Country']=='United States of America','Country',] = 'United States'
    energy.loc[energy['Country']=='United Kingdom of Great Britain and Northern Ireland','Country',] = 'United Kingdom'
    energy.loc[energy['Country']=='China, Hong Kong Special Administrative Region','Country',] = 'Hong Kong'

    GDP = pd.read_csv('world_bank.csv', skiprows=4)
    GDP.loc[GDP['Country Name']=='Korea, Rep.','Country Name',] = 'South Korea'
    GDP.loc[GDP['Country Name']=='Iran, Islamic Rep.','Country Name',] = 'Iran'
    GDP.loc[GDP['Country Name']=='Hong Kong SAR, China','Country Name',] = 'Hong Kong'

    ScimEn = pd.read_excel('scimagojr-3.xlsx').head(n=15)


    energy = energy.set_index('Country')
    GDP = GDP.set_index('Country Name')
    ScimEn = ScimEn.set_index('Country')
    stage_df = pd.merge(ScimEn, energy, how='left', left_index=True, right_index=True)
    stage_df = pd.merge(stage_df, GDP, how='left', left_index=True, right_index=True)
    stage_df = stage_df.drop(['Country Code',
       'Indicator Name', 'Indicator Code', '1960', '1961', '1962', '1963',
       '1964', '1965', '1966', '1967', '1968', '1969', '1970', '1971', '1972',
       '1973', '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981',
       '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990',
       '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999',
       '2000', '2001', '2002', '2003', '2004', '2005'], axis=1)

    return stage_df.sort_values(by='Rank', ascending=True)




# Question 2 (6.6%)
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# This function should return a single number.

def answer_two():

    eng_ind_import_df = pd.read_excel('Energy Indicators.xls', skiprows=17, skip_footer=38, names=['nuller', 'nuller2', 'Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'])
    energy = eng_ind_import_df.drop(['nuller', 'nuller2'], axis=1).replace('...',np.nan)
    energy['Energy Supply'] = energy['Energy Supply'] * 1000000
    energy['Country'] = energy['Country'].str.replace('\d+', '')
    energy['Country'] = energy['Country'].str.replace(r"\(.*\)","")

    energy.loc[energy['Country']=='Republic of Korea','Country',] = 'South Korea'
    energy.loc[energy['Country']=='Iran ','Country',] = 'Iran'
    energy.loc[energy['Country']=='United States of America','Country',] = 'United States'
    energy.loc[energy['Country']=='United Kingdom of Great Britain and Northern Ireland','Country',] = 'United Kingdom'
    energy.loc[energy['Country']=='China, Hong Kong Special Administrative Region','Country',] = 'Hong Kong'

    GDP = pd.read_csv('world_bank.csv', skiprows=4)
    GDP.loc[GDP['Country Name']=='Korea, Rep.','Country Name',] = 'South Korea'
    GDP.loc[GDP['Country Name']=='Iran, Islamic Rep.','Country Name',] = 'Iran'
    GDP.loc[GDP['Country Name']=='Hong Kong SAR, China','Country Name',] = 'Hong Kong'

    ScimEn = pd.read_excel('scimagojr-3.xlsx')


    energy = energy.set_index('Country')
    GDP = GDP.set_index('Country Name')
    ScimEn = ScimEn.set_index('Country')
    outer_df = pd.merge(ScimEn, energy, how='outer', left_index=True, right_index=True)
    outer_df = pd.merge(outer_df, GDP, how='outer', left_index=True, right_index=True)

    return len(outer_df) - len(stage_df)




# Answer the following questions in the context of only the top 15 countries by Scimagojr Rank (aka the DataFrame returned by answer_one())¶

# Question 3 (6.6%)
# What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
# This function should return a Series named avgGDP with 15 countries and their average GDP sorted in descending order.

def answer_three():
    Top15 = answer_one()
    Top15['averageGDP'] =  Top15[['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']].mean(axis=1, skipna=True)
    avgGDP = Top15['averageGDP']
    avgGDP = avgGDP.sort_values(ascending=False)

    return avgGDP




# Question 4 (6.6%)
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
# This function should return a single number.

def answer_four():

    avgGDP = answer_three()
    keys = avgGDP.index.tolist()
    avgGDP6_name = keys[5]

    Top15 = answer_one()
    avgGDP6 = Top15.loc[avgGDP6_name]

    return avgGDP6['2015'] - avgGDP6['2006']




# Question 5 (6.6%)
# What is the mean Energy Supply per Capita?
# This function should return a single number.

def answer_five():
    Top15 = answer_one()
    return Top15['Energy Supply per Capita'].mean(axis=0)




# Question 6 (6.6%)
# What country has the maximum % Renewable and what is the percentage?
# This function should return a tuple with the name of the country and the percentage.

def answer_six():

    Top15 = answer_one()
    renew_sorted = Top15.sort_values('% Renewable', ascending=False)

    greenest_countries = renew_sorted.index.tolist()
    greenest_percentage = renew_sorted['% Renewable']

    return greenest_countries[0], greenest_percentage[0]




# Question 7 (6.6%)
# Create a new column that is the ratio of Self-Citations to Total Citations. What is the maximum value for this new column, and what country has the highest ratio?
# This function should return a tuple with the name of the country and the ratio.

def answer_seven():

    Top15 = answer_one()

    Top15['new_ratio'] = Top15['Self-citations'] / Top15['Citations']
    new_rat_sorted = Top15.sort_values('new_ratio', ascending=False)

    new_rat_countries = new_rat_sorted.index.tolist()
    new_rat_percentage = new_rat_sorted['new_ratio']

    return new_rat_countries[0], new_rat_percentage[0]




# Question 8 (6.6%)
# Create a column that estimates the population using Energy Supply and Energy Supply per capita. What is the third most populous country according to this estimate?
# This function should return a single string value.

def answer_eight():

    Top15 = answer_one()

    Top15['pop_est'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    pop_est_sorted = Top15.sort_values('pop_est', ascending=False)

    pop_est_countries = pop_est_sorted.index.tolist()

    return pop_est_countries[2]




# Question 9 (6.6%)
# Create a column that estimates the number of citable documents per person. What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the .corr() method, (Pearson's correlation).
# This function should return a single number.
# (Optional: Use the built-in function plot9() to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)

def answer_nine():

    Top15 = answer_one()
    Top15['pop_est'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['cit_docs_per_person'] = Top15['Citable documents'] / Top15['pop_est']

    return Top15['cit_docs_per_person'].corr(Top15['Energy Supply per Capita'])




def plot9():

    import matplotlib as plt
    %matplotlib inline

    Top15 = answer_one()
    Top15['pop_est'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['cit_docs_per_person'] = Top15['Citable documents'] / Top15['pop_est']
    Top15.plot(x='cit_docs_per_person', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])




# Question 10 (6.6%)
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
# This function should return a series named HighRenew whose index is the country name sorted in ascending order of rank.

def answer_ten():

    Top15 = answer_one()
    med_renew_percent = Top15['% Renewable'].median(axis=0)

    Top15['HighRenew'] = ''
    Top15['HighRenew'][Top15['% Renewable'] >= med_renew_percent] = 1
    Top15['HighRenew'][Top15['% Renewable'] < med_renew_percent] = 0

    return Top15['HighRenew']




# Question 11 (6.6%)
# Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.

ContinentDict  = {'China':'Asia',
                  'United States':'North America',
                  'Japan':'Asia',
                  'United Kingdom':'Europe',
                  'Russian Federation':'Europe',
                  'Canada':'North America',
                  'Germany':'Europe',
                  'India':'Asia',
                  'France':'Europe',
                  'South Korea':'Asia',
                  'Italy':'Europe',
                  'Spain':'Europe',
                  'Iran':'Asia',
                  'Australia':'Australia',
                  'Brazil':'South America'}

# This function should return a DataFrame with index named Continent ['Asia', 'Australia', 'Europe', 'North America', 'South America'] and columns ['size', 'sum', 'mean', 'std']

def answer_eleven(ContinentDict):

    Top15 = answer_one()

    ContinentDict  = ContinentDict

    continents = pd.DataFrame(columns = ['size', 'sum', 'mean', 'std'])
    Top15['pop_est'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']

    for continent, frame in Top15.groupby(ContinentDict):
        continents.loc[continent] = [len(frame), frame['pop_est'].sum(),frame['pop_est'].mean(),frame['pop_est'].std()]

    return continents




# Question 12 (6.6%)
# Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
# This function should return a Series with a MultiIndex of Continent, then the bins for % Renewable. Do not include groups with no countries.

def answer_twelve(ContinentDict):

    Top15 = answer_one()

    ContinentDict = ContinentDict

    Top15 = Top15.reset_index()
    Top15['Continent'] = [ContinentDict[country] for country in Top15['Country']]
    Top15['bins'] = pd.cut(Top15['% Renewable'],5)

    return Top15.groupby(['Continent','bins']).size()




# Question 13 (6.6%)
# Convert the Population Estimate series to a string with thousands separator (using commas). Do not round the results.
# e.g. 317615384.61538464 -> 317,615,384.61538464
# This function should return a Series PopEst whose index is the country name and whose values are the population estimate string.

def answer_thirteen():

    Top15 = answer_one()
    Top15['pop_est'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['PopEst'] = Top15['pop_est'].map('{0:,}'.format)

    return Top15['PopEst']
