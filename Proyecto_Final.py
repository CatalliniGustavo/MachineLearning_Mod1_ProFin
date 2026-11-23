import pandas as pd
import numpy
import matplotlib.pyplot as plt

# Carga de todos los datos
emi_2016 = pd.read_csv('emisiones-2016.csv', delimiter= ';')
emi_2017 = pd.read_csv('emisiones-2017.csv', delimiter= ';')
emi_2018 = pd.read_csv('emisiones-2018.csv', delimiter= ';')
emi_2019 = pd.read_csv('emisiones-2019.csv', delimiter= ';')

# Cantidad total de la suma de todas las filas de los cuatro DataFrame
# print(emi_2016.shape[0] + emi_2017.shape[0] + emi_2018.shape[0] + emi_2019.shape[0])

# Unión de los cuatro DataFrames mediante concatenación vertical
emisiones_df = pd.concat(
    [emi_2016, emi_2017, emi_2018, emi_2019],
    axis = 0, # Apila las filas una debajo de otra
    ignore_index = True, # Descarta los índices numéricos y crea un índice continuo nuevo.
    sort = False # Mantiene el orden original de tus columnas sin reordenarlas alfabéticamente.
    )

# Filtrar columnas. Quedan 35 columnas
emisiones_df = emisiones_df.filter(
    regex=r'^(ESTACION|MAGNITUD|ANO|MES)$|^D\d+' # Toma las cuatro especificadas más las que comienzan con 'D' seguida de un número.
    )

# Aplicar .melt() para pasar las columnas de los días a filas.
emisiones_df = pd.melt(
    emisiones_df,
    id_vars = emisiones_df.filter(regex = r'^(ESTACION|MAGNITUD|ANO|MES)$'), # Las columnas que no se tocan.
    value_vars = emisiones_df.filter(regex = r'^D\d+'), # Las columnas que pasan a fila.
    var_name = 'DIA', # Nombre de la columna nueva.
    value_name = 'VALOR' # Nombre de la columna con los valores.
)
# Limpiar valores de la columna DIA sacando la 'D'
emisiones_df['DIA'] = emisiones_df['DIA'].str.lstrip('D').astype(int)

# Crear una columna con la fecha combinada con año, mes, día.
emisiones_df['FECHA'] = pd.to_datetime(
    dict(
        year = emisiones_df['ANO'],
        month = emisiones_df['MES'],
        day = emisiones_df['DIA']
    ),
    errors = 'coerce' # Coloca Nat en las filas de las fechas que no existen.
) 

# print(type(emisiones_df['FECHA'].iloc[5]))
# print(emisiones_df['FECHA'].isna().sum())
# emisiones_df.to_csv('emisiones_16_19.csv')