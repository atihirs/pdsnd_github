import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    while True:
        city_input = input("Which city do you want to analyze? Choose from chicago, new york city, or washington: ")
        city = city_input.lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print("This is not a valid choice. Please try entering the city again.")
        else:
            break

    # get user input for month (all, january, february, ... , december)
    while True:
        month_input = input("Which month do you want to analyze? If you want all months, enter ALL: ")
        month = month_input.lower()
        if month not in ('all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'):
            print("This is not a valid choice. Please try entering the month filter again.")
        else:
            break
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_input = input("Which day you want to analyze? If you want all days, enter ALL: ")
        day = day_input.lower()
        if day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
            print("This is not a valid choice. Please try entering the day filter again.")
        else:
            break
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
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
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

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    popular_month = df['month'].mode()[0]
    print("The most popular month was: ", months[popular_month-1].title())

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print("The most popular day of week was: ", popular_day_of_week)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("The most popular start hour was: ", popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("The most popular Start Station was: ", popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("The most popular End Station was: ", popular_end_station)

    # display most frequent combination of start station and end station trip
    df['Start and End Station'] = df['Start Station'] + ', ' + df['End Station']
    popular_start_end_station = df['Start and End Station'].mode()[0]
    print("The most popular Start and End Station combo was: ", popular_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total trip duration was (in seconds): ", int(df['Trip Duration'].sum()))

    # display mean travel time
    print("The average trip duration was (in seconds): ", int(df['Trip Duration'].mean()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Exclude washington from descriptive stats for gender and birth year. First display counts of gender. 
    if city != 'washington':
        gender_types = df['Gender'].value_counts()
        print(gender_types)

    # Display earliest, most recent, and most common year of birth
        print("The earliest birth year was: ", int(df['Birth Year'].min()))
        print("The most recent birth year was: ", int(df['Birth Year'].max()))
        popular_birth_year = int(df['Birth Year'].mode()[0])
        print("The most popular birth year was: ", popular_birth_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(city):
    # create new copy of dataframe from city raw data
    dr = pd.read_csv(CITY_DATA[city])
    row_index = 0
    # return 5 rows of raw data for each input
    while True:
        find_rows = input('\nIf you would like to see raw data, enter yes. Otherwise, enter anything else.\n')
        if find_rows.lower() == 'yes':
            row_view = pd.DataFrame(dr, index = range(row_index, row_index+5))
            print(row_view)
            row_index += 5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        raw_data(city)

        restart = input('\nIf you would like to restart, enter yes. Otherwise, enter anything else.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
