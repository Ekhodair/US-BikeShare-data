import time
import pandas as pd
import numpy as np
from tabulate import tabulate

CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}


def get_filters():
    """chicago
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('enter a city name you\'re interested in: Chicago, New York City or Washington!').lower()
        if city not in CITY_DATA:
            print('invalid name,\n Please enter city name as following: Chicago, New York City, Washington')

        else:
            print(f'you chose {city} to do our statistical analysis on, INTERESTING! ')
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('enter full month name between \'January\' to \'June\' (e.g. June)\
        to filter by, or "all" to apply no month filter').lower().strip()
        if month == 'all':
            print('no month filter applied')
            break
        elif month in ('january', 'february', 'march', 'april', 'may', 'june'):
            print(f'you chose {month.capitalize()} to filter by')
            break
    #  get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day= input('enter full day name (e.g. Saturday) to filter by, or "all" to apply no day filter').lower().strip()
        if day == 'all':
            print('no day filter applied')
            break
        elif day in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
            print(f'you chose {day.capitalize()} to filter by')
            break

    print('-' * 40)
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
    print('Initializing...')
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print(f'The most popular month is: {popular_month}')


    # display the most common day of week
    common_weekday= df['day_of_week'].mode()[0]
    print(f'The most common day of week is: {common_weekday}')

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    start_hour = df['hour'].mode()[0]
    print(f'The most common start hour is: {start_hour}')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print(f'The most commonly used start station: {common_start}')
    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print(f'The most common end station: {common_end}')
    # display most frequent combination of start station and end station trip
    df['start to end'] = df['Start Station'] + 'to' + df['End Station']
    start_to_end = df['start to end'].mode()[0]
    print(f'The most frequent combination of start and end stations: {start_to_end}')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print(f'Total travel time: {total_travel}')

    # display mean travel time
    avg_travel = df['Trip Duration'].mean()
    print(f'The average travel time: {avg_travel}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count = df['User Type'].value_counts()
    print(f'The count of users: {user_count}')


    # Display counts of gender
    if 'Gender' in df:
        gender_count = df['Gender'].value_counts()
        print(f'The count of Gender in users: {gender_count}')
    else:
        print('No information on gender is provided')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_year = int(df['Birth Year'].min())
        print(f'The earliest birth year: {earliest_year}')
        recent_year = int(df['Birth Year'].max())
        print(f'The most recent birth year {recent_year}')
        common_birth = int(df['Birth Year'].mode()[0])
        print(f'The most common birth common_birth year: {common_birth}')
    else:
        print("There is no birth year information in this city.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    #Display 5 rows of raw data at a time

def display_data(df):
    """
    Display raw data if requested by the user
    """
    i = 0
    while True:
        display_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n').lower().strip()
        if display_data == 'yes':
            print(tabulate(df.iloc[np.arange(0 + i, 5 + i)], headers="keys"))
            i += 5
        elif display_data == 'no':
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
