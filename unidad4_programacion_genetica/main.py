import argparse
import uvicorn
import sys
import os

# Agregamos 'src' al path para que no fallen los imports de los modelos
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def lanzar_web():
    """Inicia el dashboard con FastAPI"""
    print("\n🔥 Dashboard encendido en: http://127.0.0.1:8000")
    # reload=True hace que se reinicie solo si guardas cambios
    uvicorn.run("src.controllers.main_api:app", host="127.0.0.1", port=8000, reload=True)

def modo_consola(dataset):
    """Lógica que usará el profe para calificar"""
    print(f"\n🚀 Ejecutando evolución para el dataset: {dataset}")
    print("--- Cargando modelos de Miguel, Absalón y David ---")
    # Aquí es donde después llamaremos a la 'Evolución'
    print("Error: Falta conectar la lógica del motor.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GP Engine - Unidad 4")
    parser.add_argument("--data", type=str, help="Nombre del dataset (ej: housing)")
    
    args = parser.parse_args()

    if args.data:
        modo_consola(args.data)
    else:
        lanzar_web()