# imports required
import math
import random
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# defined variables and lists
POPULATION = 10
SIZE = 25
CENTRAL_LOCATION = 10
X = int(round((SIZE - CENTRAL_LOCATION) / 2))
Y = X + CENTRAL_LOCATION
run_number = 1
positions = list()
statuses = list()
illness_durations = list()
contact_status = list()
x_coordinates = list()
y_coordinates = list()
susceptible = list()
number = [0]
ill = [0]


# simulates the movement of individuals in the POPULATION
def positional_generation(travel_probability=25):
    for i in range(POPULATION):
        if statuses[i] == 'Deceased' or statuses[i] == 'Quarantined':
            positions[i] = positions[i]
        else:
            if random.randint(0, 100) < travel_probability:
                x_coordinate, y_coordinate = random.randrange(X, Y), random.randrange(X, Y)
            else:
                x_coordinate, y_coordinate = random.randrange(0, SIZE), random.randrange(0, SIZE)
                while X <= x_coordinate <= Y and X <= y_coordinate <= Y:
                    x_coordinate, y_coordinate = random.randrange(0, SIZE), random.randrange(0, SIZE)
            x_coordinates[i] = x_coordinate
            y_coordinates[i] = y_coordinate
            destination = f'({str(x_coordinate)}, {str(y_coordinate)})'
            positions[i] = destination


# positional generation with social distancing
def positional_generation_with_social_distancing(distancing_chance=100):
    for i in range(POPULATION):
        if statuses[i] == 'Deceased' or statuses[i] == 'Quarantined':
            positions[i] = positions[i]
        else:
            if random.randint(0, 100) < distancing_chance:
                x_coordinate, y_coordinate = random.randrange(0, SIZE), random.randrange(0, SIZE)
                while X <= x_coordinate <= Y and X <= y_coordinate <= Y:
                    x_coordinate, y_coordinate = random.randrange(0, SIZE), random.randrange(0, SIZE)
                x_coordinates[i] = x_coordinate
                y_coordinates[i] = y_coordinate
                destination = f'({str(x_coordinate)}, {str(y_coordinate)})'
                positions[i] = destination


# models the spread of the disease across the POPULATION
def infection_simulation(infection_radius=10, infection_rate=100, min_time=1, max_time=10):
    for a in range(POPULATION):
        for b in range(POPULATION):
            if math.dist([x_coordinates[a], y_coordinates[a]],
                         [x_coordinates[b], y_coordinates[b]]) <= infection_radius:
                if statuses[b] == 'Susceptible' and statuses[a] == 'Ill' and random.randint(0, 100) < infection_rate:
                    statuses[b] = 'Ill'
                    illness_durations[b] = random.randrange(min_time, max_time)


# transfers data from statuses to contact_status
def status_update():
    for i in range(POPULATION):
        if statuses[i] == 'Ill':
            contact_status[i] = 'Probable'
        elif statuses[i] == 'Recovered':
            contact_status[i] = 'Removed'
        elif statuses[i] == 'Deceased':
            contact_status[i] = 'Removed'
        elif statuses[i] == 'Quarantined':
            contact_status[i] = 'Removed'
        else:
            contact_status[i] = 'Improbable'


# simulates contacts tracing
def contact_tracing(detection_effectiveness=25, infection_radius=10):
    for a in range(POPULATION):
        for b in range(POPULATION):
            if math.dist([x_coordinates[a], y_coordinates[a]],
                         [x_coordinates[b], y_coordinates[b]]) <= infection_radius:
                if contact_status[b] == 'Improbable' and contact_status[a] == 'Probable':
                    contact_status[b] = 'Probable'
    for i in range(POPULATION):
        if contact_status[i] == 'Probable':
            if random.randint(0, 100) < detection_effectiveness:
                statuses[i], contact_status[i] = 'Quarantined', 'Improbable'


# simulates quarantine
def quarantine(detection_chance=50):
    for i in range(POPULATION):
        if statuses[i] == 'Ill' and random.randint(0, 100) < detection_chance:
            statuses[i] = 'Quarantined'


# simulates social_distancing
def social_distancing(infection_radius=10, distancing_chance=100):
    for a in range(POPULATION):
        for b in range(POPULATION):
            if random.randint(0, 100) < distancing_chance:
                while math.dist([x_coordinates[a], y_coordinates[a]],
                                [x_coordinates[b], y_coordinates[b]]) <= infection_radius and \
                        X <= x_coordinates[a] <= Y and X <= y_coordinates[a] <= Y and \
                        X <= x_coordinates[b] <= Y and X <= y_coordinates[b] <= Y:
                    x_coordinate, y_coordinate = random.randrange(0, SIZE), random.randrange(0, SIZE)
                    if statuses[a] == 'Deceased' or statuses[a] == 'Quarantined':
                        positions[b] = f'({str(x_coordinate)}, {str(y_coordinate)})'
                        x_coordinates[b], y_coordinates[b] = x_coordinate, y_coordinate
                    elif statuses[b] == 'Deceased' or statuses[b] == 'Quarantined':
                        positions[a] = f'({str(x_coordinate)}, {str(y_coordinate)})'
                        x_coordinates[a], y_coordinates[a] = x_coordinate, y_coordinate


# detects when the duration of illness ends in an individual and determines whether they recovered or died
def illness_duration_detection(mortality_rate=25):
    for i in range(POPULATION):
        if statuses[i] == 'Ill':
            illness_durations[i] = illness_durations[i] - 1
            if illness_durations[i] == 0:
                if random.randint(0, 100) <= mortality_rate:
                    statuses[i] = 'Deceased'
                    illness_durations[i] = -1
                else:
                    statuses[i] = 'Recovered'
                    illness_durations[i] = -1


# fills the predefined lists
def list_generation(min_time=1, max_time=10):
    for i in range(POPULATION):
        if i == 0:
            statuses.append('Ill')
            illness_durations.append(random.randrange(min_time, max_time))
            contact_status.append('Probable')
        else:
            statuses.append('Susceptible')
            illness_durations.append('Null')
            contact_status.append('Improbable')
        positions.append('Null')
        x_coordinates.append('Null')
        y_coordinates.append('Null')


# plots the data
def simulation_data_visualization():
    sns.set()
    fig, axes = plt.subplots(1, 2, sharex='none', sharey='none', figsize=(10, 4.5))
    plt.suptitle(f'Simulation Data For Run Number {run_number}')
    ill.append(statuses.count('Ill'))
    number.append(run_number)
    num_of_ill = pd.DataFrame()
    num_of_ill[f'Number of Active Cases: {ill[-1]}'] = ill
    sns.lineplot(ax=axes[0], data=num_of_ill)
    simulation_data = pd.DataFrame()
    simulation_data['X Coordinate'] = x_coordinates
    simulation_data['Y Coordinate'] = y_coordinates
    simulation_data['Status'] = statuses
    my_palette = {'Susceptible': '#3974bd',
                  'Ill': '#b01515',
                  'Recovered': '#148c34',
                  'Deceased': 'black',
                  'Quarantined': '#e89415'}
    x = int(round((SIZE - CENTRAL_LOCATION) / 2))
    rectangle = plt.Rectangle((x, x), CENTRAL_LOCATION, CENTRAL_LOCATION, fc='None', ec='black')
    plt.gca().add_patch(rectangle)
    sns.set(style='darkgrid')
    sns.scatterplot(ax=axes[1], x='X Coordinate', y='Y Coordinate', hue='Status',
                    data=simulation_data, palette=my_palette, legend='full')
    plt.xlim(0, SIZE)
    plt.ylim(0, SIZE)
    plt.show()


# driver code for the simulation
list_generation()
while 'Ill' in statuses:
    positional_generation_with_social_distancing()
    infection_simulation()
    illness_duration_detection()
    simulation_data_visualization()
    run_number += 1
