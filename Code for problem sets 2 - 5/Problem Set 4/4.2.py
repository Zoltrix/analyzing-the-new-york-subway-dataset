from pandas import *
from ggplot import *
from numpy import *
import datetime

# why i wrote this line
# http://stackoverflow.com/questions/18942506/add-new-column-in-pandas-dataframe-python
# http://stackoverflow.com/questions/20625582/how-to-deal-with-this-pandas-warning
pandas.options.mode.chained_assignment = None


def plot_weather_data(turnstile_weather):
    '''
    plot_weather_data is passed a dataframe called turnstile_weather.
    Use turnstile_weather along with ggplot to make another data visualization
    focused on the MTA and weather data we used in Project 3.

    Make a type of visualization different than what you did in the previous exercise.
    Try to use the data in a different way (e.g., if you made a lineplot concerning
    ridership and time of day in exercise #1, maybe look at weather and try to make a
    histogram in this exercise). Or try to use multiple encodings in your graph if
    you didn't in the previous exercise.

    You should feel free to implement something that we discussed in class
    (e.g., scatterplots, line plots, or histograms) or attempt to implement
    something more advanced if you'd like.

    Here are some suggestions for things to investigate and illustrate:
     * Ridership by time-of-day or day-of-week
     * How ridership varies by subway station
     * Which stations have more exits or entries at different times of day

    If you'd like to learn more about ggplot and its capabilities, take
    a look at the documentation at:
    https://pypi.python.org/pypi/ggplot/

    You can check out the link
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
    to see all the columns and data points included in the turnstile_weather
    dataframe.

   However, due to the limitation of our Amazon EC2 server, we are giving you a random
    subset, about 1/3 of the actual data in the turnstile_weather dataframe.
    '''

    # Ridership by day-of-week

    # add a column that represents day of weak
    mapping = lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').strftime('%A')
    turnstile_weather['day_of_week'] = turnstile_weather['DATEn'].map(mapping)

    # make the day_of_week variable a categorical one
    turnstile_weather['day_of_week'] = turnstile_weather['day_of_week'].astype('category')

    #re-order days of week, assuming that Monday is the first day of the week
    turnstile_weather['day_of_week'] = turnstile_weather['day_of_week'].cat.reorder_categories(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

    #group by day_of_week and sum ENTRIESn_hourly to get the total hourly entries for each day
    hourly_entries_day = turnstile_weather.groupby(['day_of_week'], as_index=False).aggregate(np.sum)

    #make a data frame from the aggregated results
    hourly_entries_day = DataFrame({'day_of_week': hourly_entries_day['day_of_week'],
                                    'ENTRIESn_hourly': hourly_entries_day['ENTRIESn_hourly']})

    plot = ggplot(hourly_entries_day, aes(x='day_of_week', y='ENTRIESn_hourly')) \
           +ggtitle('Entries at different days')+xlab('Day')+ylab('Total Hourly entries') \
           +geom_bar(stat='identity')

    return plot


turnstile = pandas.read_csv('turnstile_data_master_with_weather.csv')
plt = plot_weather_data(turnstile)
print plt
