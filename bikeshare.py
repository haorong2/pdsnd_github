import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def prompt_5_rows(df):
     """
    Asks user how many 5 more rows they want to view.

    """
    view_data = input('Would you like to view 5 rows of individual {} data? Enter yes or no?  '.format(df.name)).lower()
    if view_data == 'yes':
        start_loc = 0
        view_display='yes'
        while(view_display == 'yes'):
            if(start_loc <= df.value_counts().size - 5):
                print(df.value_counts()[start_loc:start_loc+5])
            else:
                print(df.value_counts()[start_loc:])
            start_loc += 5
            view_display = input('Do you wish to continue? Enter yes or no:  ').lower()



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Prompt user to input city
    validCitySelection = ['chicago', 'new york city', 'washington']
    city = 'null'
    while city not in validCitySelection:
        try:
            city = input('Enter a city you want to explore the data: ').lower()
        except ValueError:
            print('Invalid Input. Try again')
        else:
            print('Thank you for you valid input.')
        finally:
            print('You have selected {}.'.format(city))


    # Prompt user to input month
    validMonthSelection = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = 'null'
    while month not in validMonthSelection:
        try:
            month = input('Enter a month: ').lower()
        except ValueError:
            print('Invalid Input. Try again')
        else:
            print('Thank you for you valid input.')
        finally:
            print('You have selected {}.'.format(month))


    # Prompt user to input day
    validWeekdaySelection = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = 'null'
    while day not in validWeekdaySelection:
        try:
            day = input('Enter a day you want to explore the data: ').lower()
        except ValueError:
            print('Invalid Input. Try again')
        else:
            print('Thank you for you valid input.')
        finally:
            print('You have selected {}.'.format(day))


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

    # Display the most common month
    print('The most common month: {}'.format(df['month'].mode()[0]))

    # Display the most common day of week
    print('The most common day of week: {}'.format(df['day_of_week'].mode()[0]))

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('The most common month: {}'.format(df['hour'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    prompt_5_rows(df['Start Station'])


    print('The Most Popular Start Station - {}, {} times\n\n\n'.format(df['Start Station'].value_counts().index[0], df['Start Station'].value_counts()[0]))


    # Display most commonly used end station
    prompt_5_rows(df['End Station'])
    print('\nThe Most Popular End Station - {}, {} times\n\n\n'.format(df['End Station'].value_counts().index[0], df['End Station'].value_counts()[0]))

    # Display most frequent combination of start station and end station trip
    df['Start-End Route'] = df['Start Station'] + ' --- ' + df['End Station']
    prompt_5_rows(df['Start-End Route'])
    print('\nThe Most Popular Route - {}, {} times\n\n\n'.format(df['Start-End Route'].value_counts().index[0], df['Start-End Route'].value_counts()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    print(df['Trip Duration'].sum())


    # Display mean travel time
    print(df['Trip Duration'].mean())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df:
        print(df['Gender'].value_counts())
    else:
        print('Gender stats cannot be calculated because Gender does not appear in the dataframe')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('The earliest year of birth: {}'.format(df['Birth Year'].min()))
        print('The most recent year of birth: {}'.format(df['Birth Year'].max()))
        print('The most common year of birth: {}'.format(df['Birth Year'].mode()[0]))
    else:
        print('Birth Year stats cannot be calculated because Birth Year does not appear in the dataframe')

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

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
