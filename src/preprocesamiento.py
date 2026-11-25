import pandas as pd

# DataFrame original unificado
def cargar_datos(archivos: list) -> pd.DataFrame:
    return pd.concat((pd.read_csv(f) for f in archivos), ignore_index=True)

# DataFrame filtrado
def filtrar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    df = df.filter(
    regex = r'^(ESTACION|MAGNITUD|ANO|MES)$|^D\d+') # Toma las cuatro especificadas más las que comienzan con 'D' seguida de un número.
    return df

# DataFrame en formato largo
def reestructurar_datos(df: pd.DataFrame) -> pd.DataFrame:
    df = df.melt(
        id_vars = df.filter(regex = r'^(ESTACION|MAGNITUD|ANO|MES)$').columns, # Las columnas que no se tocan.
        value_vars = df.filter(regex = r'^D\d+').columns, # Las columnas que pasan a fila.
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
    df = df.dropna(subset=["FECHA"]).reset_index(drop=True) # Elimina las filas Nat de la columna 'FECHA'.
    return df.sort_values(by=["ESTACION", "FECHA"]).reset_index(drop=True) # Ordena los datos por estaciones y fecha.
    
# DataFrame final	Coordinación
def preprocesar_datos(archivos: list[str]) -> pd.DataFrame:
    df = cargar_datos(archivos)
    df = filtrar_columnas(df)
    df = reestructurar_datos(df)
    df = columna_fecha(df)
    df = limpiar_datos(df)
    return df
    
from pathlib import Path

# ruta_data = Path(__file__).resolve().parents[1] / "data"
# archivos_csv = sorted(ruta_data.glob("*.csv"))
# print(archivos_csv)
# data\emisiones-2016.csv
archivos = [f.as_posix() for f in sorted(Path("data").glob("*.csv"))]
print(preprocesar_datos(archivos))