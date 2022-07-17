import numpy as np
import random
import matplotlib.pyplot as plt


class KSP:
    initialPopulation = 100
    birthRate = 0.3
    deathRate = 0.03
    birthRateDev = 0.03
    deathRateDev = 0.01
    humanInfluenceRate = 0.2
    humanInfluenceDev = 0.025
    resourcesRate = 0.05
    resourcesDev = 0.01
    phenomenonRate = 0.1
    phenomenonDev = 0.05


class KPI:
    populationSize = 0
    newBirths = 0
    newDeaths = 0
    humanInfluence = False
    humanDeaths = 0
    resources = True
    resourceDeaths = 0
    phenomenon = False
    phenomenonDeaths = 0


def get_num_births(num_hippos, birth_rate_mean, birth_rate_dev):
    """
    This function returns the number of new born hippo calfs in one year,
    sing a random number, which is calculated through the normalvariate.

    :param num_hippos: An integer, representing the current number of hippos
    :param birth_rate_mean: A double between 0 and 1, representing the average birth rate of hippos
    :param birth_rate_dev: A double between 0 and 1, the standard deviation for the average birth rate
    :return: An integer, the number of new born hippos
    """
    births = random.normalvariate(birth_rate_mean, birth_rate_dev)
    new_births = num_hippos * births
    return int(new_births)


def get_num_deaths(num_hippos, death_rate_mean, death_rate_dev):
    """
    This function returns the number of hippos dying each year 'naturally',
    sing a random number, which is calculated through the normalvariate.

    :param num_hippos: An integer, representing the current number of hippos
    :param death_rate_mean: A double between 0 and 1, representing the average death rate of hippos
    :param death_rate_dev: A double between 0 and 1, the standard deviation for the average death rate
    :return: An integer, the number of hippos died 'naturally'
    """
    deaths = random.normalvariate(death_rate_mean, death_rate_dev)
    new_deaths = num_hippos * deaths
    return int(new_deaths)


def get_num_human_deaths(num_hippos, human_influence_mean, human_influence_dev):
    """
    This function returns the number of hippos dying by human influence each year,
    sing a random number, which is calculated through the normalvariate.

    :param num_hippos: An integer, representing the current number of hippos
    :param human_influence_mean: A double between 0 and 1, representing the average percentage of hippos,
        humans try to kill each year.
    :param human_influence_dev: A double between 0 and 1, the standard deviation for the human_influence_mean
    :return: An integer, the number of hippos that were killed by human influence
    """
    death_rate = random.normalvariate(human_influence_mean, human_influence_dev)
    new_deaths = num_hippos * death_rate
    return int(new_deaths)


def get_num_resource_deaths(num_hippos, resources_mean, resources_dev):
    """
    This function returns the number of hippos dying because of not enough resources each year,
    using a random number, which is calculated through the normalvariate.

    :param num_hippos: An integer, representing the current number of hippos.
    :param resources_mean: A double between 0 and 1, representing the average percentage of hippos,
        that die each year because of not enough resources.
    :param resources_dev: A double between 0 and 1, the standard deviation for the resources_mean
    :return: An integer, the number of hippos that died because of not enough resources
    """
    death_rate = random.normalvariate(resources_mean, resources_dev)
    new_deaths = num_hippos * death_rate
    return int(new_deaths)


def get_num_phenomenon_deaths(num_hippos, phenomenon_mean, phenomenon_dev):
    """
    This function returns the number of hippos dying as a consequence of random phenomena (e.g., weather),
    using a random number, which is calculated through the normalvariate.

    :param num_hippos: An integer, representing the current number of hippos.
    :param phenomenon_mean: A double between 0 and 1, representing the average percentage of hippos,
        that die each year because of random phenomenon.
    :param phenomenon_dev: A double between 0 and 1, the standard deviation for the phenomenon_mean
    :return: An integer, the number of hippos that died because of random phenomena
    """
    death_rate = random.normalvariate(phenomenon_mean, phenomenon_dev)
    new_deaths = num_hippos * death_rate
    return int(new_deaths)


def is_there_human_influence(num_hippos, current_year):
    """
    This function answers the question if there is human influence in a specific year.
    In the first three years of the simulation humans will not be ready to regulate the system,
    so they will not start regulation before year 3. Also there is no need for regulation,
    if the number of hippos is below 400.

    :param num_hippos: An integer, representing the current number of hippos.
    :param current_year: An integer, representing the current year of the simulation
    :return: A boolean, returns True if there will be human influence, otherwise it returns False.
    """
    if current_year < 3: return False
    else:
        if num_hippos < 400: return False
        else: return True


def enough_resources(num_hippos, current_year):
    """
    This function answers the question if there are enough resources for the hippos in a specific year.
    In the first 20 years of the simulation there will be enough resources if the number of hippos stays
    under 1000. Between 20 and 50 years there are enough resources if there are under 500 hippos.
    In every other case there are not enough resources.

    :param num_hippos: An integer, representing the current number of hippos.
    :param current_year: An integer, representing the current year of the simulation
    :return: A boolean, returns True if there are enough resources, otherwise it returns False.
    """
    if current_year < 20 and num_hippos < 1000: return True
    elif 20 < current_year < 50 and num_hippos < 500: return True
    else: return False


def is_there_phenomenon(current_year):
    """
    This function answers the question if there is a random phenomenon in a specific year.
    Since a random phenomenon is independent of the hippo population, we just look if a
    random number between 1 and 300 is smaller than the current year. That also will raise the
    probability of a phenomenon the more far we look into the future (which makes sense).

    :param current_year: An integer, representing the current year of the simulation
    :return: A boolean, returns True if there is a random phenomenon this year, otherwise it returns False.
    """
    random_number = random.randint(1, 300)
    if random_number < current_year:
        return True
    else: return False


def simulate(num_years):
    """
    This is the central function of our program. Using the classes KSP (Key System Parameters) and
    KPI (Key Performance Indicators) we simulate the population growth of the hippos,
    under the influence of many parameters described by the previous functions.

    :param num_years: An integer, representing the amount of years we want to simulate.
    :return: An array, which represents the hippo population over all years.
    """
    hippo_population = []

    ksp = KSP()
    kpi = KPI()

    kpi.populationSize = ksp.initialPopulation

    for current_year in range(num_years):
        if kpi.populationSize <= 0: break

        kpi.newBirths = get_num_births(kpi.populationSize, ksp.birthRate, ksp.birthRateDev)
        kpi.newDeaths = get_num_deaths(kpi.populationSize, ksp.deathRate, ksp.deathRateDev)

        kpi.humanInfluence = is_there_human_influence(kpi.populationSize, current_year)
        if kpi.humanInfluence: kpi.humanDeaths = get_num_human_deaths(kpi.populationSize, ksp.humanInfluenceRate, ksp.humanInfluenceDev)
        else: kpi.humanDeaths = 0

        kpi.resources = enough_resources(kpi.populationSize, current_year)
        if kpi.resources: kpi.resourceDeaths = 0
        else: kpi.resourceDeaths = get_num_resource_deaths(kpi.populationSize, ksp.resourcesRate, ksp.resourcesDev)

        kpi.phenomenon = is_there_phenomenon(current_year)
        if kpi.phenomenon: kpi.phenomenonDeaths = get_num_phenomenon_deaths(kpi.populationSize, ksp.phenomenonRate, ksp.phenomenonDev)
        else: kpi.phenomenonDeaths = 0

        kpi.populationSize = kpi.populationSize + kpi.newBirths - kpi.newDeaths - kpi.humanDeaths - kpi.resourceDeaths - kpi.phenomenonDeaths

        hippo_population.append(kpi.populationSize)

    return hippo_population


def get_carrying_capacity(num, years):
    """
    This function gives us the searched carrying capacity, by using the mean of a number of arrays,
    which are already calculated means of a number of maximum values (= carrying capacity) of a
    number of simulations. So the the resulting carrying capacity is representative.

    :param num: An integer, representing the amount of simulations to do, using num^2 simulations
    :param years: An integer, representing the amount of years the simulation should hold on.
    :return: An integer, representing the carrying capacity for num^2 simulations.
    """
    maximum = 0
    array = []
    result = []

    for i in range(num):
        for j in range(num):
            sim = simulate(years)
            x = max(sim)
            array.append(x)
            maximum = np.mean(array)

        result.append(maximum)

    carrying_capacity = int(np.mean(result))
    return carrying_capacity


def logistic_growth(growth_rate, initial_population, carrying_capacity, num_years):
    """
    This function returns the logistic growth of a population growth.

    :param growth_rate: A double, between 0 and 1, representing the growth rate
    :param initial_population: An integer, the amount of population at the beginning.
        ATTENTION: This parameter is not the same as in the KSP class!
    :param carrying_capacity: An integer, representing the carrying capacity
    :param num_years: An integer, representing the number of years of the growth function
    :return: An array, representing the population growth over the years.
    """
    population = []

    for t in range(num_years):
        p = carrying_capacity / (1 + (carrying_capacity - initial_population) / initial_population * np.exp(-1 * growth_rate * t))
        population.append(p)

    return population


def experiment1(growth_rate, initial_population, num_simulations, num_years):
    """
    This function is our main experiment. Here we use a lot of simulations to find
    a reasonable carrying capacity value. Using this value we then use the logistic growth
    function using the parameters and the carrying capacity to plot the population growth.

    :param growth_rate: A double between 0 and 1, representing the growth rate.
    :param initial_population: An integer, representing the initial population-
    :param num_simulations: An integer, representing the number of simulations we will perform,
        with using num_simulations^2.
    :param num_years: An integer, representing the number of years the growth function should be plotted.
    """
    index = []
    carrying_capacity_array = []

    carrying_capacity = get_carrying_capacity(num_simulations, num_simulations)

    population = logistic_growth(growth_rate, initial_population, carrying_capacity, num_years)
    for elem in range(len(population)):
        index.append(elem + 2020)
        carrying_capacity_array.append(carrying_capacity)

    title = "Population Growth with rate r = " + str(growth_rate)
    carrying_capacity_str = "K = " + str(carrying_capacity)

    plt.plot(index, population, label = "Population Growth")
    plt.plot(index, carrying_capacity_array, color = "r", label = "Carrying Capacity")
    plt.legend(loc = "lower right", prop = {'size': 12})
    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel("Number of Hippos")
    plt.annotate(carrying_capacity_str, xy = (2030, carrying_capacity - 10), xytext = (2030, carrying_capacity - 400),
                 arrowprops = dict(facecolor='red', shrink=0.05),)
    plt.show()


def experiment2(num_years):
    """
    This experiment is used to get an overview about how possible simulations can look like.
    Here just 5 example simulations will run and then plotted into the same plot.

    :param num_years: An integer, representing the amount of years that should be plotted.
    """
    index = []
    for elem in range(num_years):
        index.append(elem)

    population1 = simulate(num_years)
    population2 = simulate(num_years)
    population3 = simulate(num_years)
    population4 = simulate(num_years)
    population5 = simulate(num_years)

    plt.plot(index, population1, label = "Simulation 1")
    plt.plot(index, population2, label = "Simulation 2")
    plt.plot(index, population3, label = "Simulation 3")
    plt.plot(index, population4, label = "Simulation 4")
    plt.plot(index, population5, label = "Simulation 5")
    plt.legend(loc = "upper left", prop = {'size': 9})
    plt.title("Average amount of Hippos over time")
    plt.xlabel("Years")
    plt.ylabel("Number of Hippos")
    plt.show()


"""
Run experiment 1 to plot the logistic growth function for the hippo population,
by passing the arguments growth_rate, initial_population, num_simulations and num_years like that:
experiment1(growth_rate, initial_population, num_simulations, num_years)
"""
#experiment1(0.05, 100, 100, 150)


"""
Run experiment 2 to plot five random simulations over a couple of years,
by passing the argument num_years like that: experiment2(num_years).
"""
#experiment2(100)