# imports externs
import numpy as np
import pandas as pd
import os
import random


# imports interns: llibreria de funcionalitats
def dues_direccions(dataset):
    """Afegeix files al set de dades tal que les connexions entre
    nodes es tinguin en conta en les dues direccions."""
    llista_cols = list(dataset.columns)

    # Usem els indexs per a intercanviar les columnes "Node" i "Node2"
    llista_cols[2], llista_cols[3] = llista_cols[3], llista_cols[2]
    auxiliar = dataset[llista_cols]

    return pd.concat([auxiliar, dataset], ignore_index=True)


def centralitat_elastica(data):
    """Calcula la centralitat dels nodes donada una taula de dades."""
    k = 30
    gamma = 0.98
    ec_node = 0
    ec_temps = 0

    # iterem sobre les dades
    for temps, accio in zip(data['Time'], data['Type']):

        # actualitzem la variable si ha passat suficient temps
        if ec_temps >= k:
            ec_node = ec_node * gamma ** k

        # tractem les dades segons l'acció que pren lloc
        if accio == 'up':
            ec_node += 1
        if accio == 'down':
            ec_temps = temps - ec_temps

    return pd.Series({'EC': ec_node})


def trobar_mitjana(temps):
    """Calcula la mitja per parelles donada una llista de valor."""
    if len(temps) == 0:
        return 0

    temps = temps.tolist()

    # Troba cada parella, computa el temps entre accions i retorna la mitjana
    t_connectats = 0
    for i in range(0, len(temps), 2):
        inici = temps[i]
        final = temps[i + 1]
        t_connectats += (final - inici)

    return t_connectats / (len(temps) / 2)


def mitjana_entre_conns(temps):
    """Calcula la mitjana de temps entre diferents connexions (ICT)"""
    # Si la llargada de la llista és parell, llavors l'ultima fila tindrà com
    # a acció 'down', per tant, treiem l'entrada fet que volem parelles inverses
    if len(temps) % 2 == 0:
        temps = temps[:-1]

    # Treiem la primera filera per a tenir les parelles inverses de connexions
    temps = temps[1:]

    return trobar_mitjana(temps)


def mitjana_duracio_conns(temps):
    """Calcula la mitja de temps entre connexions (DURC)"""
    # Si la llargada de la llista no és parell, l'ultima connexio no ha
    # acabat, i per tal de no tenir un infinit, treiem dita entrada
    if len(temps) % 2 != 0:
        temps = temps[:-1]

    return trobar_mitjana(temps)
