import pandas as pd
import qgrid
import matplotlib.pyplot as plt
import matplotlib.dates as dates

#  Importing economic calendar
df = pd.read_csv('EconomicCalendar.csv')
df.columns = ['Date', 'Currency', 'Impact', 'Event', 'Actual', 'Forecast',
              'Previous']
df.Date = pd.to_datetime(df.Date)
# df.Date = dates.date2num(df.Date)

#  Remove no and low impact rows, remove votes beacuse of #format not convertable
df = df[df.Impact != 'Non-Economic']

event_filter = ['Asset Purchase Facility Votes', 'Official Bank Rate Votes']
df = df.loc[~df['Event'].str.contains('|'.join(event_filter))]

for col in ['Actual', 'Forecast', 'Previous']:
    #  Remove rows with certain formats not convertable
    df = df.loc[~df[col].str.contains('|'.join(['\|', '\<']), na=False)]

    #  Change %, K, M, B, T into numerics
    df.loc[pd.notnull(df[col]) & df[col].str.contains('\%'), col] = \
        pd.to_numeric(df.loc[pd.notnull(df[col]) & df[col].str.contains(
            '\%'), col].str.replace('%', '')) / 100
    df.loc[pd.notnull(df[col]) & df[col].str.endswith('K'), col] = \
        pd.to_numeric(df.loc[pd.notnull(df[col]) & df[col].str.endswith(
            'K'), col].str.replace('K', '')) * 1000
    df.loc[pd.notnull(df[col]) & df[col].str.endswith('M'), col] = \
        pd.to_numeric(df.loc[pd.notnull(df[col]) & df[col].str.endswith(
            'M'), col].str.replace('M', '')) * 1000000
    df.loc[pd.notnull(df[col]) & df[col].str.endswith('B'), col] = \
        pd.to_numeric(df.loc[pd.notnull(df[col]) & df[col].str.endswith(
            'B'), col].str.replace('B', '')) * 1000000000
    df.loc[pd.notnull(df[col]) & df[col].str.endswith('T'), col] = \
        pd.to_numeric(df.loc[pd.notnull(df[col]) & df[col].str.endswith(
            'T'), col].str.replace('T', '')) * 1000000000000

    #  Change all to numeric to perform calculation
    df[col] = pd.to_numeric(df[col])

# Creating Surprise column which is Actual minus Forecast
df['Surprise'] = df['Actual'] - df['Forecast']

#  Choose impact factor and currency to show
impact = ['High', 'Medium']
currency = ['EUR']

output = df.loc[df.Impact.str.contains('|'.join(impact))]
# The line above has no purpose, since in the line below you immediately
# reassign the variable 'output'.
output = df.loc[df.Currency.str.contains('|'.join(currency))]

#  Plot output
grouped = output.groupby('Event')

for i in grouped.groups.keys():
    print("Graph Title: " + i) # This prints the title of the graph
    print(output.loc[output.Event.str.contains(i)]['Actual'])
    # Notice that the program (only?) crashes when all the values are NaN.
    output.loc[output.Event.str.contains(i)].plot(x='Date', y='Actual',
                                                  title=i)
    plt.show()

