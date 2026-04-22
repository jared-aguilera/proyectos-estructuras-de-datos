import pandas as pd
import numpy as np
import os

class DataLoader:
    
    @staticmethod
    def cargar_dataset(nombre_dataset):
        """carga archivos csv o data sin encabezados"""
        ruta_csv = f"data/{nombre_dataset}.csv"
        ruta_data = f"data/{nombre_dataset}.data"
        
        # intentamos cargar el csv primero, luego el .data
        if os.path.exists(ruta_csv):
            # header=None evita que se pierda la primera fila de datos
            df = pd.read_csv(ruta_csv, header=None)
        elif os.path.exists(ruta_data):
            # sep='\s+' sirve para archivos .data con espacios
            df = pd.read_csv(ruta_data, sep='\s+', header=None)
        else:
            raise FileNotFoundError(f"No se encontro {nombre_dataset} en data/")
        
        # limpieza de valores nulos
        df = df.dropna()

        # X son todas las columnas menos la ultima, y es la ultima columna
        X = df.iloc[:, :-1].values
        y = df.iloc[:, -1].values
        
        return X, y