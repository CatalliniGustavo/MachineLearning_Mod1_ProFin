import pandas as pd
import numpy
import matplotlib.pyplot as plt

# Carga de todos los datos
emi_2016 = pd.read_csv('emisiones-2016.csv', delimiter= ';')
emi_2017 = pd.read_csv('emisiones-2017.csv', delimiter= ';')
emi_2018 = pd.read_csv('emisiones-2018.csv', delimiter= ';')
emi_2019 = pd.read_csv('emisiones-2019.csv', delimiter= ';')

# Cantidad total de la suma de todas las filas de los cuatro DataFrame
print(emi_2016.shape[0] + emi_2017.shape[0] + emi_2018.shape[0] + emi_2019.shape[0])

# Unión de los cuatro DataFrames mediante concatenación vertical
emisiones_df = pd.concat(
    [emi_2016, emi_2017, emi_2018, emi_2019],
    axis = 0,
    ignore_index = True,
    sort = False
    )
