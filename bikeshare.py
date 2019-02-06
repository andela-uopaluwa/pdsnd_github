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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_is_valid = False
    while not(city_is_valid):
        city = input('Enter city name of choice from "Chicago, New York City, Washington": ').strip().lower()
        city_is_valid = validate_input_filters(city, ['chicago', 'new york city', 'washington'])

    # get user input for month (all, january, february, ... , june)
    month_is_valid = False
    while not(month_is_valid):
        month = input('Enter month of choice from "january, february, march, april, may, june" or "all": ').strip().lower()
        month_is_valid = validate_input_filters(month, ['january', 'february', 'march', 'april', 'may', 'june', 'all'])

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_is_valid = False
    while not(day_is_valid):
        day = input('Enter the day of week of choice from "monday, tuesday, wednesday, thursday, friday, saturday, sunday" or "all": ').strip().lower()
        day_is_valid = validate_input_filters(day, ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'])

    print('-'*40)
    return city, month, day

def validate_input_filters(user_input, valid_data_set):
    if user_input in valid_data_set:
        return True
    else:
        print("Invalid Input! Try Again")

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
    city = city.replace(" ", "_")
    df = pd.read_csv('{}.csv'.format(city))
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    df = df[df['month'] == month.title()] if month != 'all' else df
    df = df[df['day_of_week'] == day.title()] if day != 'all' else df
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    print("Most common month for trips: ", ', '.join(df['month'].mode().values))

    # display the most common day of week
    print("Most common day of the week for trips: ", ', '.join(df['day_of_week'].mode().values))

    # display the most common start hour
    print("Most common start hour for trips: {}".format(df['hour'].mode().values))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most common start station for trips: ", ', '.join(df["Start Station"].mode().values))

    # display most commonly used end station
    print("Most common end station for trips: ", ', '.join(df["End Station"].mode().values))

    # display most frequent combination of start station and end station trip
    df['route'] = df["Start Station"] + " - " + df["End Station"]
    print("Most frequent combination of start station and end station trip: ", ', '.join(df['route'].mode().values))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time_summary = {
        "days": total_travel_time // 86400,
        "hours": (total_travel_time % 86400) // 3600,
        "minutes": (total_travel_time % 3600) // 60 , 
        "seconds": total_travel_time % 60 
    }

    print("Total travel time is {} seconds and is equivalent to {} day(s) {} hour(s) {} minutes(s) {} second(s)".format(total_travel_time, total_travel_time_summary["days"], 
    total_travel_time_summary["hours"], total_travel_time_summary["minutes"], total_travel_time_summary["seconds"]))

    # display mean travel time
    print("Average travel time is {} seconds".format( df['Trip Duration'].mean() ))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("User types and their count: ")
    print(df['User Type'].value_counts())

    if city == 'washington':
        print("Gender and Birth Year data are not available for {}".format(city.title()))
    else:
        # Display counts of gender
        print("Gender count: ")
        print(df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth
        birth_data = (df['Birth Year'].dropna(axis=0)).astype('int64')
        print('Earliest Birth Year: {}'.format(birth_data.min()))
        print('Most Recent Birth Year: {}'.format(birth_data.max()))
        print('Most Common Birth Year: {}'.format(*birth_data.mode().values))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_dataset(df):
    """Displays loaded data based on user response."""
    start, end = 0, 0
    display_data = input("Type 'yes' if you would like to see 5 rows of the dataset or 'no' to continue: ").strip().lower()
    while display_data == 'yes':
        end += 5
        print(df[start:end])
        start = end
        display_data = input("Type 'yes' if you would like to see 5 more rows of the dataset or 'no' to continue: ").strip().lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        print_dataset(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
