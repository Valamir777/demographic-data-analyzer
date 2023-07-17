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
    raceList_count = pd.Series(data=race_Count, index=raceList)
    return raceList_count


def filter_rows_by_values(df, col, values):
    """
    :param df: Data Frame of Population Demographics
    :param col: Column to be filtered
    :param values: Value to be filtered out of the Column
    :return: A filtered version of the Data Frame
    """
    return df[~df[col].isin(values)]


def menAvg_age(df, Gender):
    """
    :param Gender:
    :param df: Data Frame of Population Demographics
    :return: Returns the Average age of Males from the Data Set as a rounded whole integer
    """
    dfCopy = filter_rows_by_values(df, 'sex', Gender)
    return round(dfCopy['age'].mean(), 1)


def Education_percent(df, education_level):
    """

    :param df: Data frame of population Demographics.
    :param education_level: Level of education to be filtered.
    :return: filtered percentage of those having the education level.
    """
    total_population = df.shape[0]
    lst = list(set(df['education'].unique().tolist()) - set(education_level))
    educated_population = filter_rows_by_values(df, 'education', lst).shape[0]
    return float("{:10.1f}".format((educated_population / total_population) * 100))


def income_class(df, education_level, income_level):
    """
    :param df: Demographic Data Frame
    :param education_level: Education level of Demographics to be observed
    :param income_level: Income level of Demographics to be observed
    :return: Percentage of Educated Demographic earning greater than Input Level
    """

    educated_population = filter_rows_by_values(df, 'education',
                                                list(set(df['education'].unique().tolist()) - set(education_level)))
    income_population = filter_rows_by_values(educated_population, 'salary',
                                              list(set(educated_population['salary'].unique().tolist())
                                                   - set(income_level)))
    return float("{:10.1f}".format((income_population.shape[0] / educated_population.shape[0] * 100)))


def minWorking_hours(df):
    hours_worked = df['hours-per-week'].tolist()
    hours_worked.sort()
    return hours_worked[0]


def minWorking_hoursHigh_Salary(df):
    salary = ['>50K']
    minHours_worked = [minWorking_hours(df)]
    minimumHour_workers = filter_rows_by_values(df, 'hours-per-week',
                                                list(
                                                    set(df['hours-per-week'].unique().tolist()) - set(minHours_worked)))

    minWorkers_salaryTypes = minimumHour_workers['salary'].unique().tolist()
    salaryFilter = list(set(minWorkers_salaryTypes) - set(salary))
    minHour_workersHigh_Salary = filter_rows_by_values(minimumHour_workers, 'salary', salaryFilter)
    return float("{:10.1f}".format((minHour_workersHigh_Salary.shape[0] / minimumHour_workers.shape[0] * 100)))


def nationalsHigh_income(df, nation, nations):
    lowIncome = df['salary'].unique().tolist()
    lowIncome.remove('>50K')
    nationsCopy = nations.copy()
    nationsCopy.remove(nation)
    nf = filter_rows_by_values(df, 'native-country', nationsCopy)
    nf = filter_rows_by_values(nf, 'salary', lowIncome)
    return nf


def highest_earningCountry(df):
    nation_earnings = dict()
    # Create list of 42 Nations
    nationList = df['native-country'].unique().tolist()
    for nation in nationList:
        nation_earnings[nation] = nationalsHigh_income(df, nation, nationList).shape[0]
    return nation_earnings


def highestEarning_countryPercentage(df, nation_earnings):
    nationHighest_percentage = dict()
    nationList = df['native-country'].unique().tolist()
    for nation in nationList:
        nationList_copy = nationList.copy()
        nationList_copy.remove(str(nation))
        nationPopulation = filter_rows_by_values(df, 'native-country', nationList_copy)
        nationHighest_percentage[nation] = nation_earnings[nation] / (nationPopulation.shape[0]) * 100
    return max(nationHighest_percentage, key=nationHighest_percentage.get), \
           float("{:10.1f}".format(nationHighest_percentage[max(nationHighest_percentage,
                                                                key=nationHighest_percentage.get)]))


def popularOccupation(income_df):
    occupations = income_df['occupation'].unique().tolist()
    occupation_Count = []
    for occupation in occupations:
        occupation_Count.append(list(income_df['occupation']).count(str(occupation)))
    occupations_count = pd.Series(data=occupation_Count, index=occupations)
    return occupations_count.index[occupations_count.argmax()]


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')
    # Assign Two variable for educated population and uneducated.
    educatedPopulation = ['Bachelors', 'Masters', 'Doctorate']
    uneducatedPopulation = ['HS-grad', '11th', '9th', 'Some-college', 'Assoc-acdm',
                            'Assoc-voc', '7th-8th', 'Prof-school', '5th-6th', '10th',
                            '1st-4th', 'Preschool', '12th']

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the
    # index labels.
    race_count = raceCount(df)

    # What is the average age of men?
    average_age_men = menAvg_age(df, ['Female'])

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = Education_percent(df, ['Bachelors'])

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = Education_percent(df, educatedPopulation)
    lower_education = Education_percent(df, uneducatedPopulation)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # percentage with salary >50K
    higher_education_rich = income_class(df, educatedPopulation, ['>50K'])
    lower_education_rich = income_class(df, uneducatedPopulation, ['>50K'])

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = minWorking_hours(df)

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    rich_percentage = minWorking_hoursHigh_Salary(df)

    # What country has the highest percentage of people that earn >50K?
    highest_earning_country = highestEarning_countryPercentage(df, highest_earningCountry(df))[0]
    highest_earning_country_percentage = highestEarning_countryPercentage(df, highest_earningCountry(df))[1]

    # Identify the most popular occupation for those who earn >50K in India.
    top_IN_occupation = popularOccupation(nationalsHigh_income(df, 'India', df['native-country'].unique().tolist()))


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
