import numpy as np
import time
from gplearn.genetic import SymbolicRegressor 
from src.utils.data_loader import DataLoader
from src.models.engine import Evaluador

def ejecutar_benchmark_profesional(nombre_dataset):
    print(f"\n--- Iniciando Benchmark: {nombre_dataset} ---")
    
    loader = DataLoader()
    X, y = loader.cargar_dataset(nombre_dataset)
    
    print("Ejecutando motor propio (5 vueltas)...")
    
    mses_gp = []
    tiempos_gp = []
    
    print("Ejecutando gplearn (5 vueltas para estadística)...")
    for i in range(5): 
        gp = SymbolicRegressor(
            population_size=500,
            generations=50,
            tournament_size=7,
            p_crossover=0.9,
            p_subtree_mutation=0.1,
            random_state=i 
        )
        
        inicio = time.time()
        gp.fit(X, y)
        fin = time.time()
        
        y_pred = gp.predict(X)
        mse = np.mean((y - y_pred)**2)
        mses_gp.append(mse)
        tiempos_gp.append(fin - inicio)
        
    print(f"\nRESULTADOS GPLEARN ({nombre_dataset}):")
    print(f"Media MSE: {np.mean(mses_gp):.4f}")
    print(f"Desviación Estándar MSE: {np.std(mses_gp):.4f}")
    print(f"Tiempo Promedio: {np.mean(tiempos_gp):.2f}s")

if __name__ == "__main__":
    datasets = ["concrete", "tower", "yacht", "housing", "energy_cooling", "energy_heating"]

    ejecutar_benchmark_profesional(datasets[0])