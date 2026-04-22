from src.utils.data_loader import DataLoader

try:
    print("--- Cargando dataset de Concreto ---")
    X, y = DataLoader.cargar_dataset("concrete")
    
    print(f"✅ ¡Éxito! Datos cargados.")
    print(f"Dimensiones de X (Variables): {X.shape}") # Debería ser (1030, 8)
    print(f"Dimensiones de y (Target): {y.shape}")     # Debería ser (1030,)
    print(f"Primer fila de X: {X[0]}")
    print(f"Primer valor de y: {y[0]}")

except Exception as e:
    print(f"❌ Error al cargar: {e}")