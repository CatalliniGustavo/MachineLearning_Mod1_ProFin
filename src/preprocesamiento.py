from pathlib import Path

import pandas as pd


# Gestiona la lista de archivos que cumplan con los requisitos para ser procesados
# Listar archivos disponibles
def lista_archivos() -> list[str]:
    archivos = [
        f.as_posix() for f in sorted(Path("data").glob("*.csv"))
    ]  # Carga la ruta de todos los archivos CSV de la carpeta 'data'
    columnas_fijas = {
        "ESTACION",
        "MAGNITUD",
        "ANO",
        "MES",
    }  # Columnas mínimas para poder operar
    columnas_dias = {
        f"D{i:02d}" for i in range(1, 32)
    }  # Genera {'D01', 'D02', ..., 'D31'} debe tener al menos una en ese intervalo

    lista_csv = []
    csv_rechazados = []
    # Filtra los archivos y anuncia los que se descartan
    for f in archivos:
        columnas_csv = set(
            pd.read_csv(f, sep=";", nrows=0).columns.tolist()
        )  # Solo las columnas del archivo CSV
        if columnas_fijas.issubset(columnas_csv) and not columnas_dias.isdisjoint(
            columnas_csv
        ):  # Las cuatro columnas mínimas y al menos 1 de los días
            lista_csv.append(f)
        else:
            csv_rechazados.append(f.split("/")[-1])
            print(f"Descartado: {f}")  # Los archivos que no cumplen con los requisitos

    print(f"{len(csv_rechazados)} archivos rechazados: {csv_rechazados}")
    # Si la lista está vacía
    if not lista_csv:
        raise ValueError(
            "Ningún archivo en 'data/' cumplió con las columnas requeridas."
        )
    csv_aceptados = ", ".join(f.split("/")[-1] for f in lista_csv)
    print(
        f"{len(lista_csv)} de {len(archivos)} archivos habilitados para la evaluación: {csv_aceptados}"
    )
    return lista_csv


# DataFrame original unificado
def cargar_datos(archivos: list[str]) -> pd.DataFrame:
    df = pd.concat((pd.read_csv(f, sep=";") for f in archivos), ignore_index=True)
    return df


# DataFrame filtrado
def filtrar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    df = df.filter(
        regex=r"^(ESTACION|MAGNITUD|ANO|MES)$|^D\d+"
    )  # Toma las cuatro especificadas más las que comienzan con 'D' seguida de un número.
    return df


# DataFrame en formato largo
def reestructurar_datos(df: pd.DataFrame) -> pd.DataFrame:
    df = df.melt(
        id_vars=df.filter(
            regex=r"^(ESTACION|MAGNITUD|ANO|MES)$"
        ).columns,  # Las columnas que no se tocan.
        value_vars=df.filter(
            regex=r"^D\d+"
        ).columns,  # Las columnas que se transforman en filas.
        var_name="DIA",  # Nombre de la columna nueva.
        value_name="VALOR",  # Nombre de la columna con los valores.
    )
    return df


# DataFrame con fechas
def columna_fecha(df: pd.DataFrame) -> pd.DataFrame:
    df["DIA"] = (
        df["DIA"].str.lstrip("D").astype(int)
    )  # Limpiar valores de la columna DIA sacando la 'D'
    df["FECHA"] = pd.to_datetime(
        dict(year=df["ANO"], month=df["MES"], day=df["DIA"]),
        errors="coerce",  # Coloca Nat en las filas de las fechas que no existen.
    )
    return df


# DataFrame depurado y ordenado
def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=["FECHA"])  # Elimina las filas NaT de la columna 'FECHA'.
    return df.sort_values(by=["ESTACION", "FECHA"]).reset_index(
        drop=True
    )  # Ordena los datos por estaciones y fecha.


# DataFrame final	Coordinación
def preprocesar_datos() -> pd.DataFrame:
    archivos = lista_archivos()
    df = cargar_datos(archivos)
    df = filtrar_columnas(df)
    df = reestructurar_datos(df)
    df = columna_fecha(df)
    df = limpiar_datos(df)
    return df