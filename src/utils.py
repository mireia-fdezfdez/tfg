# external imports
import numpy as np
import pandas as pd
import os


# internal imports
def both_ways(dataset):  # TODO. Optimize function
    """Adds rows to the dataset so that a connection between to nodes is
    counted in both directions"""
    column_list = list(dataset.columns)

    # Use the indices to swap the columns of "Node" and "Node2"
    column_list[2], column_list[3] = column_list[3], column_list[2]
    auxiliar = dataset[column_list]
    dataset = pd.concat([auxiliar, dataset], ignore_index=True)

    return dataset


def find_mean(temps):
    """Calculates the mean pair value given a list"""
    # If there is no info in the list, then there is no full circle of connections
    # and so provisionally, we count as 0 (because we cannot divide by 0 later)
    if len(temps) == 0:
        return 0

    temps = temps.tolist()

    # Find each pair, compute the time between items and return its mean value
    t_connected = 0
    for i in range(0, len(temps), 2):
        inici = temps[i]
        final = temps[i + 1]
        t_connected += (final - inici)

    return t_connected / (len(temps) / 2)


def mean_btw_conns(temps):
    """To calculate the mean time between different connections (ICT)"""
    # If the list is even then the last value is a "down" item and we take it
    # down to not disturb the calculations
    if len(temps) % 2 == 0:
        temps = temps[:-1]

    # We take down the first item in the list, so we have inverse pairs to calculate
    # the time mean
    temps = temps[1:]

    return find_mean(temps)


def mean_conn_duration(temps):
    """To calculate the mean time of the connection's duration (DURC)"""
    # If the list is not even then the last communication did not conclude
    # provisionally, we take it down
    if len(temps) % 2 != 0:
        temps = temps[:-1]

    return find_mean(temps)
