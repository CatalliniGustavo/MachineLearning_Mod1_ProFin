import pandas as pd
from pathlib import Path

# Listar archivos disponibles
def lista_archivos() -> list[str]:
    archivos = [f.as_posix() for f in sorted(Path("data").glob("*.csv"))]
    columnas_fijas = {'ESTACION','MAGNITUD','ANO','MES'} # Columnas minimas para poder operar 
    columnas_dias = {f'D{i:02d}' for i in range(1, 32)}  # Genera {'D01', 'D02', ..., 'D31'} debe tener almenos una en ese intervalo
    
    listaCSV = []
    for f in archivos:
        CSV_columnas = set(pd.read_csv(f, sep=';', nrows=0).columns.tolist())
        if columnas_fijas.issubset(CSV_columnas) and not columnas_dias.isdisjoint(CSV_columnas):
            listaCSV.append(f)
        else:
            print(f"Descartado: {f}")
    assert len(listaCSV) > 0, "Ningún archivo cumplió con los requisitos."
    return listaCSV

# DataFrame original unificado
def cargar_datos(archivos: list[str]) -> pd.DataFrame:  
    df = pd.concat((pd.read_csv(f, sep=';') for f in archivos), ignore_index=True)
    return df

# DataFrame filtrado
def filtrar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    df = df.filter(
    regex = r'^(ESTACION|MAGNITUD|ANO|MES)$|^D\d+') # Toma las cuatro especificadas más las que comienzan con 'D' seguida de un número.
    return df

# DataFrame en formato largo
def reestructurar_datos(df: pd.DataFrame) -> pd.DataFrame:
    df = df.melt(
        id_vars = df.filter(regex = r'^(ESTACION|MAGNITUD|ANO|MES)$').columns, # Las columnas que no se tocan.
        value_vars = df.filter(regex = r'^D\d+').columns, # Las columnas que se transforman en filas.
        var_name = 'DIA', # Nombre de la columna nueva.
        value_name = 'VALOR', # Nombre de la columna con los valores.
        )
    return df

# DataFrame con fechas
def columna_fecha(df: pd.DataFrame) -> pd.DataFrame:
    df['DIA'] = df['DIA'].str.lstrip('D').astype(int) # Limpiar valores de la columna DIA sacando la 'D'
    df['FECHA'] = pd.to_datetime(
        dict(
            year = df['ANO'],
            month = df['MES'],
            day = df['DIA']),
        errors = 'coerce' # Coloca Nat en las filas de las fechas que no existen.
        )
    return df

# DataFrame depurado y ordenado
def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=["FECHA"]) # Elimina las filas NaT de la columna 'FECHA'.
    return df.sort_values(by=["ESTACION", "FECHA"]).reset_index(drop=True) # Ordena los datos por estaciones y fecha.
    
# DataFrame final	Coordinación
def preprocesar_datos() -> pd.DataFrame:
    archivos = lista_archivos()
    df = cargar_datos(archivos)
    df = filtrar_columnas(df)
    df = reestructurar_datos(df)
    df = columna_fecha(df)
    df = limpiar_datos(df)
    return df
    

# Test
print(preprocesar_datos())