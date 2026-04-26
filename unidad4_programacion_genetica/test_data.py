from src.utils.data_loader import DataLoader

try:
    print("--- Cargando dataset de Concreto ---")
    X, y = DataLoader.cargar_dataset("concrete")
    
    print(f"Bien - Datos cargados.")
    print(f"Dimensiones de X (Variables): {X.shape}") 
    print(f"Dimensiones de y (Target): {y.shape}")    
    print(f"Primer fila de X: {X[0]}")
    print(f"Primer valor de y: {y[0]}")

except Exception as e:
    print(f"Error al cargar: {e}")