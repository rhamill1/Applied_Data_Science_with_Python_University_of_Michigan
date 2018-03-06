import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

# Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the pandas documentation to find functions or methods you might not have used yet, or ask questions on Stack Overflow and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.

# Definitions:

# A quarter is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# A recession is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# A recession bottom is the quarter within a recession which had the lowest GDP.
# A university town is a city which has a high percentage of university students compared to the total population of the city.
# Hypothesis: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (price_ratio=quarter_before_recession/recession_bottom)

# The following data files are available for this assignment:

# From the Zillow research data site there is housing data for the United States. In particular the datafile for all homes at a city level, City_Zhvi_AllHomes.csv, has median home sale prices at a fine grained level.
# From the Wikipedia page on college towns is a list of university towns in the United States which has been copy and pasted into the file university_towns.txt.
# From Bureau of Economic Analysis, US Department of Commerce, the GDP over time of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file gdplev.xls. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# Each function in this assignment below is worth 10%, with the exception of run_ttest(), which is worth 50%.

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}




def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ],
    columns=["State", "RegionName"]  )

    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''

    import_uni_towns_df = pd.read_table('university_towns.txt', skiprows=0, names=['raw_text'])

    university_towns = []

    for index, row in import_uni_towns_df.iterrows():

        messy_state_city_uni = row['raw_text']

        if 'edit' in messy_state_city_uni:
            state = messy_state_city_uni

        else:
            city = messy_state_city_uni
            university_towns.append([state, city])

    final_df = pd.DataFrame(university_towns,columns = ['State','RegionName'])

    final_df['State']=final_df['State'].str.replace('\[edit\]','')
    final_df['RegionName'] = final_df['RegionName'].str.replace(r" \(.*","")
    final_df['RegionName'] = final_df['RegionName'].str.replace('\[.*\]','')


    return final_df




def get_recession_start():
    '''Returns the year and quarter of the recession start time as a
    string value in a format such as 2005q3'''

    gdp_import_df = pd.read_excel('gdplev.xls', skiprows=219,
                                  names=['null1', 'null2', 'null3', 'null4', 'year_q', 'gdp_cur_dol', 'gdp_billions_2009_dollars', 'null5'])
    gdp_import_df = gdp_import_df.drop(['null1', 'null2', 'null3', 'null4','gdp_cur_dol', 'null5'], axis=1)
    gdp_import_df['gdp_delta'] = gdp_import_df['gdp_billions_2009_dollars'] - gdp_import_df['gdp_billions_2009_dollars'].shift(1)

    for index, row in gdp_import_df.iterrows():

        if row['gdp_delta'] < 0 and gdp_import_df.iloc[index - 1]['gdp_delta'] < 0:
            return gdp_import_df.iloc[index - 1]['year_q']




def get_recession_end():
    '''Returns the year and quarter of the recession end time as a
    string value in a format such as 2005q3'''

    recession_start = get_recession_start()
    recession_start = recession_start[:4] + recession_start[-1]

    gdp_import_df = pd.read_excel('gdplev.xls', skiprows=219,
                                  names=['null1', 'null2', 'null3', 'null4', 'year_q', 'gdp_cur_dol', 'gdp_billions_2009_dollars', 'null5'])
    gdp_import_df = gdp_import_df.drop(['null1', 'null2', 'null3', 'null4','gdp_cur_dol', 'null5'], axis=1)
    gdp_import_df['gdp_delta'] = gdp_import_df['gdp_billions_2009_dollars'] - gdp_import_df['gdp_billions_2009_dollars'].shift(1)

    gdp_import_df['year_q_math'] = gdp_import_df['year_q'].apply(lambda x: x[:4] + x[-1])

    gdp_working_df = gdp_import_df.where(gdp_import_df['year_q_math'] >= recession_start).dropna().reset_index()
    gdp_working_df = gdp_working_df.drop(['index'], axis=1)

    for index, row in gdp_working_df.iterrows():

        if row['gdp_delta'] > 0 and gdp_working_df.iloc[index - 1]['gdp_delta'] > 0:
            return row['year_q']




def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a
    string value in a format such as 2005q3'''


    recession_start = get_recession_start()
    recession_start = recession_start[:4] + recession_start[-1]

    gdp_import_df = pd.read_excel('gdplev.xls', skiprows=219,
                                  names=['null1', 'null2', 'null3', 'null4', 'year_q', 'gdp_cur_dol', 'gdp_billions_2009_dollars', 'null5'])
    gdp_import_df = gdp_import_df.drop(['null1', 'null2', 'null3', 'null4','gdp_cur_dol', 'null5'], axis=1)
    gdp_import_df['gdp_delta'] = gdp_import_df['gdp_billions_2009_dollars'] - gdp_import_df['gdp_billions_2009_dollars'].shift(1)

    gdp_import_df['year_q_math'] = gdp_import_df['year_q'].apply(lambda x: x[:4] + x[-1])

    gdp_working_df = gdp_import_df.where(gdp_import_df['year_q_math'] >= recession_start).dropna().reset_index()
    gdp_working_df = gdp_working_df.drop(['index'], axis=1)

    for index, row in gdp_working_df.iterrows():

        if row['gdp_delta'] > 0 and gdp_working_df.iloc[index - 1]['gdp_delta'] < 0:
            return gdp_working_df.iloc[index - 1]['year_q']




def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].

    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.

    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''

    states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

    city_housing_import_df = pd.read_csv('City_Zhvi_AllHomes.csv')
    city_housing_df = city_housing_import_df[['State', 'RegionName',
        '2000-01',  '2000-02',  '2000-03',  '2000-04',  '2000-05',  '2000-06',  '2000-07',  '2000-08',  '2000-09',  '2000-10',  '2000-11',  '2000-12',  '2001-01',  '2001-02',  '2001-03',  '2001-04',  '2001-05',  '2001-06',  '2001-07',  '2001-08',  '2001-09',  '2001-10',  '2001-11',  '2001-12',  '2002-01',  '2002-02',  '2002-03',  '2002-04',  '2002-05',  '2002-06',  '2002-07',  '2002-08',  '2002-09',  '2002-10',  '2002-11',  '2002-12',  '2003-01',  '2003-02',  '2003-03',  '2003-04',  '2003-05',  '2003-06',  '2003-07',  '2003-08',  '2003-09',  '2003-10',  '2003-11',  '2003-12',  '2004-01',  '2004-02',  '2004-03',  '2004-04',  '2004-05',  '2004-06',  '2004-07',  '2004-08',  '2004-09',  '2004-10',  '2004-11',  '2004-12',  '2005-01',  '2005-02',  '2005-03',  '2005-04',  '2005-05',  '2005-06',  '2005-07',  '2005-08',  '2005-09',  '2005-10',  '2005-11',  '2005-12',  '2006-01',  '2006-02',  '2006-03',  '2006-04',  '2006-05',  '2006-06',  '2006-07',  '2006-08',  '2006-09',  '2006-10',  '2006-11',  '2006-12',  '2007-01',  '2007-02',  '2007-03',  '2007-04',  '2007-05',  '2007-06',  '2007-07',  '2007-08',  '2007-09',  '2007-10',  '2007-11',  '2007-12',  '2008-01',  '2008-02',  '2008-03',  '2008-04',  '2008-05',  '2008-06',  '2008-07',  '2008-08',  '2008-09',  '2008-10',  '2008-11',  '2008-12',  '2009-01',  '2009-02',  '2009-03',  '2009-04',  '2009-05',  '2009-06',  '2009-07',  '2009-08',  '2009-09',  '2009-10',  '2009-11',  '2009-12',  '2010-01',  '2010-02',  '2010-03',  '2010-04',  '2010-05',  '2010-06',  '2010-07',  '2010-08',  '2010-09',  '2010-10',  '2010-11',  '2010-12',  '2011-01',  '2011-02',  '2011-03',  '2011-04',  '2011-05',  '2011-06',  '2011-07',  '2011-08',  '2011-09',  '2011-10',  '2011-11',  '2011-12',  '2012-01',  '2012-02',  '2012-03',  '2012-04',  '2012-05',  '2012-06',  '2012-07',  '2012-08',  '2012-09',  '2012-10',  '2012-11',  '2012-12',  '2013-01',  '2013-02',  '2013-03',  '2013-04',  '2013-05',  '2013-06',  '2013-07',  '2013-08',  '2013-09',  '2013-10',  '2013-11',  '2013-12',  '2014-01',  '2014-02',  '2014-03',  '2014-04',  '2014-05',  '2014-06',  '2014-07',  '2014-08',  '2014-09',  '2014-10',  '2014-11',  '2014-12',  '2015-01',  '2015-02',  '2015-03',  '2015-04',  '2015-05',  '2015-06',  '2015-07',  '2015-08',  '2015-09',  '2015-10',  '2015-11',  '2015-12',  '2016-01',  '2016-02',  '2016-03',  '2016-04',  '2016-05',  '2016-06',  '2016-07',  '2016-08']]


    for month in city_housing_df.columns:
        if '20' in month:

            new_quarter = month[:4] + 'q' + str(pd.to_datetime(month).quarter)
            city_housing_df.rename(columns={month: new_quarter}, inplace=True)

    city_housing_df = city_housing_df.set_index(['State', 'RegionName'])
    city_housing_df = city_housing_df.groupby(by=city_housing_df.columns, axis=1).mean()
    city_housing_df = city_housing_df.reset_index()

    city_housing_df['State'] = city_housing_df['State'].map(states)
    city_housing_df.set_index(['State', 'RegionName'],inplace=True)

    return city_housing_df




def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values,
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence.

    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''


    # ID Recession Data
    recession_start = get_recession_start()
    recession_start = recession_start[:4] + recession_start[-1]

    gdp_import_df = pd.read_excel('gdplev.xls', skiprows=219,
                                  names=['null1', 'null2', 'null3', 'null4', 'year_q', 'gdp_cur_dol', 'gdp_billions_2009_dollars', 'null5'])
    gdp_import_df = gdp_import_df.drop(['null1', 'null2', 'null3', 'null4','gdp_cur_dol', 'null5'], axis=1)
    gdp_import_df['gdp_delta'] = gdp_import_df['gdp_billions_2009_dollars'] - gdp_import_df['gdp_billions_2009_dollars'].shift(1)

    gdp_import_df['year_q_math'] = gdp_import_df['year_q'].apply(lambda x: x[:4] + x[-1])

    gdp_working_df = gdp_import_df.where(gdp_import_df['year_q_math'] >= recession_start).dropna().reset_index()
    gdp_working_df = gdp_working_df.drop(['index'], axis=1)


    for index, row in gdp_working_df.iterrows():

        if row['gdp_delta'] > 0 and gdp_working_df.iloc[index - 1]['gdp_delta'] < 0:
            bottom_quarter_math =  gdp_working_df.iloc[index - 1]['year_q_math']
            break

    gdp_working_df = gdp_working_df.where(gdp_working_df['year_q_math'] <= bottom_quarter_math).dropna().reset_index()
    gdp_working_df = gdp_working_df.drop(['index'], axis=1)
    gdp_working_df = gdp_working_df.set_index(['year_q'])
    gdp_working_df['recession_scope'] = 1


    # ID housing data
    city_housing_import_df = pd.read_csv('City_Zhvi_AllHomes.csv')
    city_housing_df = city_housing_import_df[['State', 'RegionName',
        '2000-01',  '2000-02',  '2000-03',  '2000-04',  '2000-05',  '2000-06',  '2000-07',  '2000-08',  '2000-09',  '2000-10',  '2000-11',  '2000-12',  '2001-01',  '2001-02',  '2001-03',  '2001-04',  '2001-05',  '2001-06',  '2001-07',  '2001-08',  '2001-09',  '2001-10',  '2001-11',  '2001-12',  '2002-01',  '2002-02',  '2002-03',  '2002-04',  '2002-05',  '2002-06',  '2002-07',  '2002-08',  '2002-09',  '2002-10',  '2002-11',  '2002-12',  '2003-01',  '2003-02',  '2003-03',  '2003-04',  '2003-05',  '2003-06',  '2003-07',  '2003-08',  '2003-09',  '2003-10',  '2003-11',  '2003-12',  '2004-01',  '2004-02',  '2004-03',  '2004-04',  '2004-05',  '2004-06',  '2004-07',  '2004-08',  '2004-09',  '2004-10',  '2004-11',  '2004-12',  '2005-01',  '2005-02',  '2005-03',  '2005-04',  '2005-05',  '2005-06',  '2005-07',  '2005-08',  '2005-09',  '2005-10',  '2005-11',  '2005-12',  '2006-01',  '2006-02',  '2006-03',  '2006-04',  '2006-05',  '2006-06',  '2006-07',  '2006-08',  '2006-09',  '2006-10',  '2006-11',  '2006-12',  '2007-01',  '2007-02',  '2007-03',  '2007-04',  '2007-05',  '2007-06',  '2007-07',  '2007-08',  '2007-09',  '2007-10',  '2007-11',  '2007-12',  '2008-01',  '2008-02',  '2008-03',  '2008-04',  '2008-05',  '2008-06',  '2008-07',  '2008-08',  '2008-09',  '2008-10',  '2008-11',  '2008-12',  '2009-01',  '2009-02',  '2009-03',  '2009-04',  '2009-05',  '2009-06',  '2009-07',  '2009-08',  '2009-09',  '2009-10',  '2009-11',  '2009-12',  '2010-01',  '2010-02',  '2010-03',  '2010-04',  '2010-05',  '2010-06',  '2010-07',  '2010-08',  '2010-09',  '2010-10',  '2010-11',  '2010-12',  '2011-01',  '2011-02',  '2011-03',  '2011-04',  '2011-05',  '2011-06',  '2011-07',  '2011-08',  '2011-09',  '2011-10',  '2011-11',  '2011-12',  '2012-01',  '2012-02',  '2012-03',  '2012-04',  '2012-05',  '2012-06',  '2012-07',  '2012-08',  '2012-09',  '2012-10',  '2012-11',  '2012-12',  '2013-01',  '2013-02',  '2013-03',  '2013-04',  '2013-05',  '2013-06',  '2013-07',  '2013-08',  '2013-09',  '2013-10',  '2013-11',  '2013-12',  '2014-01',  '2014-02',  '2014-03',  '2014-04',  '2014-05',  '2014-06',  '2014-07',  '2014-08',  '2014-09',  '2014-10',  '2014-11',  '2014-12',  '2015-01',  '2015-02',  '2015-03',  '2015-04',  '2015-05',  '2015-06',  '2015-07',  '2015-08',  '2015-09',  '2015-10',  '2015-11',  '2015-12',  '2016-01',  '2016-02',  '2016-03',  '2016-04',  '2016-05',  '2016-06',  '2016-07',  '2016-08']]

    for month in city_housing_df.columns:
        if '20' in month:

            new_quarter = month[:4] + 'q' + str(pd.to_datetime(month).quarter)
            city_housing_df.rename(columns={month: new_quarter}, inplace=True)

    city_housing_df = city_housing_df.set_index(['State', 'RegionName'])
    city_housing_df = city_housing_df.groupby(by=city_housing_df.columns, axis=1).mean()
    city_housing_df = city_housing_df.reset_index()

    city_housing_df['State'] = city_housing_df['State'].map(states)
    city_housing_df.set_index(['State', 'RegionName'],inplace=True)

    college_towns_df = get_list_of_university_towns()
    college_towns_df['college_town_flag'] = 1
    college_towns_df.set_index(['State', 'RegionName'],inplace=True)


    # Join sets
    working_df = pd.merge(city_housing_df, college_towns_df, how='left', left_index=True, right_index=True)
    working_df = working_df.T
    working_df = pd.merge(working_df, gdp_working_df, how='left', left_index=True, right_index=True)
    working_df = working_df.T


    # recession formating and filtering
    recess_df = working_df[['2008q3', '2008q4', '2009q1', '2009q2', 'college_town_flag']]
    recess_df = recess_df[:-4]
    recess_df['up_down'] = (recess_df['2008q3'] - recess_df['2009q2'])/recess_df['2008q3']
    recess_df = recess_df.drop(['2008q3', '2008q4', '2009q1', '2009q2'], axis=1)


    # create test sets
    recess_college_df = recess_df[recess_df['college_town_flag']==1].loc[:,'up_down'].dropna()
    recess_non_college_df = recess_df[recess_df['college_town_flag']!=1].loc[:,'up_down'].dropna()


    # run ttest
    ttest_results = ttest_ind(recess_college_df, recess_non_college_df)
    ttest_result_p = ttest_results[-1]
    diff = ttest_result_p < .01

    return (diff, ttest_result_p, 'university town')
