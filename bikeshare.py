import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months_data = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

daysofweek_data = ['monday', 'tuesday', 'wednesday', 'thursday',
                   'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('City (Chicago, New York City, or Washington):\n').lower()
    while city not in CITY_DATA.keys():
        city = input('Please type again: ').lower()


    # get user input for month (all, january, february, ... , june)
    month = input('Month (January, February, March, April, May, June, or All):\n').lower()
    while month not in months_data:
        month = input('Please type again: ').lower()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Day of week (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or All):\n').lower()
    while day not in daysofweek_data:
        day = input('Please type again: ').lower()


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])


    # display the most common month
    # extract month from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month

    # find the most popular month
    popular_month = df['month'].mode()[0]

    print('Most Popular Start Month: {}'.format(months_data[popular_month-1].title()))


    # display the most common day of week
    # extract dayofweek from the Start Time column to create a dayofweek column
    df['dayofweek'] = df['Start Time'].dt.dayofweek

    # find the most popular month
    popular_dayofweek = df['dayofweek'].mode()[0]

    print('Most Popular Start Day of Week: {}'.format(daysofweek_data[popular_dayofweek].title()))


    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour: {}'.format(popular_hour))


    print("\nThis took {} seconds.".format(time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()


    # display most commonly used start station
    popular_station_start = df['Start Station'].mode()[0]
    print('Most commonly used start station: {}'.format(popular_station_start))


    # display most commonly used end station
    popular_station_end = df['End Station'].mode()[0]
    print('Most commonly used end station: {}'.format(popular_station_end))


    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' - ' + df['End Station']
    popular_trip = df['Trip'].mode()[0]
    print('Most frequent trip: {}'.format(popular_trip))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()


    # display total travel time
    print('Total travel time: {} seconds.'.format(df['Trip Duration'].sum()))


    # display mean travel time
    print('Mean travel time: {} seconds.'.format(df['Trip Duration'].mean()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    # Display counts of user types
    user_types = df['User Type'].value_counts()
    # print value counts for each user type
    print(user_types)


    # Gender information
    if 'Gender' not in df:
        print('Gender data not available.')
    else:
        # Display counts of gender
        gender = df['Gender'].value_counts()
        # print value counts for gender
        print(gender)


    # Birthyear information
    if 'Birth Year' not in df:
        print('Birth Year data not available.')
    else:
        # Display earliest, most recent, and most common year of birth
        print('Earliest year of birth: {}'.format(df['Birth Year'].min()))
        print('Most recent year of birth: {}'.format(df['Birth Year'].max()))
        print('Most common year of birth: {}'.format(df['Birth Year'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)


        # Print raw data
        raw_data = input('\nWould you like to print 5 lines of raw data? Enter yes or no.\n')
        count = 0
        nlines = df.shape[0]
        while raw_data.lower() == 'yes':
            print(df[:][count:count+5])
            raw_data = input('\nPrint additional 5 lines of raw data? Enter yes or no.\n')
            count += 5
            # Check if the counter reaches the number of lines of the raw data
            if count+5 > nlines-1:
                print('\nMaximum number of lines reached!\n')
                break


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
