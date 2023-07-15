import pandas as pd


def raceCount(df):
    """
    :param df: Takes a data frame of population demographics, finds each instance of a unique race occurring,
    counts each occurrence of those races and zips the unique races to their total count in a dictionary.
    :return: a Dictionary of unique races and the total amount of each race represented in the Data.
    """
    raceList = df['race'].unique()
    race_Count = []
    for Race in raceList:
        race_Count.append(list(df['race']).count(str(Race)))
    return dict(zip(raceList, race_Count))


def filter_rows_by_values(df, col, values):
    """
    :param df: Data Frame of Population Demographics
    :param col: Column to be filtered
    :param values: Value to be filtered out of the Column
    :return: A filtered version of the Data Frame
    """
    return df[~df[col].isin(values)]


def menAvg_age(df):
    """
    :param df: Data Frame of Population Demographics
    :return: Returns the Average age of Males from the Data Set as a rounded whole integer
    """
    dfCopy = filter_rows_by_values(df, 'sex', ['Female'])
    return int(dfCopy['age'].mean())


def bachelorsEducation_percent(df):
    total_population = df.shape[0]
    # Create list of all education types and remove Bachelors from the list
    list = df['education'].unique().tolist()
    list.remove('Bachelors')
    bachelors_population = filter_rows_by_values(df, 'education', list).shape[0]
    return '{:,.2%}'.format(bachelors_population/total_population)


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')
    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the
    # index labels.
    race_count = raceCount(df)

    # What is the average age of men?
    average_age_men = menAvg_age(df)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = bachelorsEducation_percent(df)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = None
    lower_education = None

    # percentage with salary >50K
    higher_education_rich = None
    lower_education_rich = None

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = None

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = None

    rich_percentage = None

    # What country has the highest percentage of people that earn >50K?
    highest_earning_country = None
    highest_earning_country_percentage = None

    # Identify the most popular occupation for those who earn >50K in India.
    top_IN_occupation = None

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
            highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
