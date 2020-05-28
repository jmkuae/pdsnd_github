import calendar
import time
import datetime
import pandas as pd
import numpy as np
import os 

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (int) month - month number to filter by, or 0 to apply no month filter
        (int) day of the week - numeric day of week to filter by, or 7 to not apply any day filter
    """
    print('='*50)
    print('\n   Hello! Let\'s explore some US bikeshare data!\n')
    print('='*50)
    print(' ')

    error_message1 = '\nInvalid city number!\nPlease enter a valid city number according to the options\n'
    error_message2 = '\nInvalid month number!\nPlease enter a valid month number according to the options!\n'
    error_message3 = '\nInvalid day of the week!\nPlease enter a valid day of the week according to the options!\n'

    # Get user city
    valid = False
    while valid == False:
        try:
            print('Select a city to analyse:\n')
            print('1 - Chicago')
            print('2 - New York City')
            print('3 - Washington')
            city = int(input("\nEnter city number: "))
            if city == 1 or city == 2 or city == 3:
                valid = True
                print(' ')
            else:
                print(error_message1)           
        except KeyboardInterrupt:
             break
        except:
            print(error_message1)                
    if city == 1:
        city = 'chicago'
    elif city == 2:
        city = 'new york city'
    elif city == 3:
        city = 'washington'

    # Get user month
    valid = False
    while valid == False:
        try:        
            print('Select month to analyse using the month number:\n')
            print('0 - All months')
            print('1 - January')
            print('2 - February')
            print('3 - March')
            print('4 - April')
            print('5 - May')
            print('6 - June')
            print('7 - July')
            print('8 - August')
            print('9 - September')
            print('10 - Octorber')
            print('11 - November')
            print('12 - December')
            month = int(input("\nEnter month number: "))
            if month in range(0,13):
                valid = True
                print(' ')
            else:
                print(error_message2)           
        except KeyboardInterrupt:
             break
        except:
            print(error_message2)                

    # Get user day of week
    valid = False
    while valid == False:
        try:        
            print('Enter day of the week according to the number:\n')                        
            print('0 - Monday')
            print('1 - Tuesday')
            print('2 - Wednesday')
            print('3 - Thursday')
            print('4 - Friday')
            print('5 - Saturday')
            print('6 - Sunday')
            print('7 - All days')
            day = int(input("\nEnter day of the week: "))
            if day in range(0,8):
                valid = True
                print(' ')
            else:
                print(error_message3)           
        except KeyboardInterrupt:
             break
        except:
            print(error_message3)

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (int) month - month number to filter by, or 0 to apply no month filter
        (int) day of the week - numeric day of the week to filter by, or 7 to not apply any day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour
    df['start end station']=df['Start Station']+' / '+df['End Station']
    df['duration'] = df['End Time'] - df['Start Time']

    # Filter DataFrame according to filters
    #Filtering by month
    if month != 0:
        df = df[df['month'] == month]

    #Filtering by day of the week
    if day != 7:
        df = df[df['day_of_week'] == day]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    popular_month = df['month'].mode()[0]
    print('Most popular month: {}'.format(datetime.date(1900, popular_month, 1).strftime('%B')))

    # Display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('Most popular day of the week: {}'.format(calendar.day_name[popular_day_of_week]))

    # Display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour: {} hr'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most popular start station: {}'.format(popular_start_station))

    # Display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most popular end station: {}'.format(popular_end_station))

    # Display most frequent combination of start station and end station trip
    popular_start_end_station=df['start end station'].mode()[0]
    print('Most popular start and end station: {}.'.format(popular_start_end_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_duration = df['duration'].sum()
    print('Total travel time: {}.'.format(total_duration))

    # Display mean travel time
    mean_duration = df['duration'].mean()
    print('Mean travel time: {}.'.format(mean_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df,city):
    """
    Displays statistics on bikeshare users.
    Args:
        (dataframe) df - data
        (str) city - name of the city to analyze
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types 
    user_types = df['User Type'].value_counts()
    for type in user_types.index: 
        print('{}  -  {} user(s)'.format(type, user_types[type])) 

    # Display counts of gender - only available for NYC and Chicago
    if city != 'washington':
        genders = df['Gender'].value_counts()
        for gender in genders.index: 
            print('{}  -  {} user(s)'.format(gender, genders[gender])) 

    # Display earliest, most recent, and most common year of birth - only available for NYC and Chicago
        print('Earliest year of birth: {}'.format(int(df['Birth Year'].min())))
        print('Most recent year of birth: {}'.format(int(df['Birth Year'].max())))
        print('Most common year of birth: {}'.format(int(df['Birth Year'].mode()[0])))

    else: # city is Washington
        print(' ')
        print('No gender and year of birth information for Washington')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_raw_data(df):
    print(' ')
    raw_data = 'yes'
    page = 1
    row = 1
    while raw_data == 'yes':    
        while row <= page * 5:
            print('ID: {}'.format(df.iloc[row,0]))
            print('Start Time: {}'.format(df.iloc[row,1]))
            print('End Time: {}'.format(df.iloc[row,2]))
            print('Trip Duration: {}'.format(df.iloc[row,3]))            
            if  pd.notna(df.iloc[row,4]):
                print('Start Station: {}'.format(df.iloc[row,4]))
            if  pd.notna(df.iloc[row,5]):
                print('End Station: {}'.format(df.iloc[row,5]))
            if  pd.notna(df.iloc[row,6]):
                print('User Type: {}'.format(df.iloc[row,6]))
            if 'Gender' in df:
                if  pd.notna(df.iloc[row,7]):
                    print('Gender: {}'.format(df.iloc[row,7]))
            if 'Birth Year' in df:
                if  pd.notna(df.iloc[row,8]):
                    print('Birth Year: {}'.format(int(df.iloc[row,8])))
            print(' ')
            row += 1

        try:
            print('Would you like to see additional raw data?')
            raw_data = input('Type "yes" to see additional raw data:')
            page += 1
        except KeyboardInterrupt:
            break
        except:
            print('Please enter a valid answer') 

def main():
    while True:
        os.system('cls')
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if df.size > 0:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df,city)
            print(' ')
            print('Would you like to see the raw data?') 
            print_data =input('Type "yes" if you want to see the raw data: ')
            if print_data.lower() == 'yes':
                print_raw_data(df)
        else:
            print('\nUsing the filters entered, there is no US bikeshare data\n') 

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()