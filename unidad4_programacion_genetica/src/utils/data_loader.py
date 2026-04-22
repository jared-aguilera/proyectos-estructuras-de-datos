import pandas as pd
import numpy as np

class DataLoader:
    
    @staticmethod
    def cargar_dataset(nombre_dataset):
        """carga archivos csv asumiendo que la ultima columna es el target"""
        ruta = f"data/{nombre_dataset}.csv"
        
        df = pd.read_csv(ruta)
        
        X = df.iloc[:, :-1].values
        y = df.iloc[:, -1].values
        
        return X, y