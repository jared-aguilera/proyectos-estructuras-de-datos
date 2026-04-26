import argparse
import uvicorn
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def lanzar_web():
    """Inicia el dashboard con FastAPI"""
    print("\n[INFO] Dashboard encendido en: http://127.0.0.1:8000")
    # reload=True hace que se reinicie solo si guardas cambios
    uvicorn.run("src.controllers.main_api:app", host="127.0.0.1", port=8000, reload=True)

def modo_consola(dataset, gens, pop, cross, mut, tour):
    from src.models.engine import GeneticEngine
    
    print(f"\n[INFO] Ejecutando evolución para el dataset: {dataset}")
    print(f"Parámetros: Generaciones={gens}, Población={pop}, Cruce={cross}, Mutación={mut}, Torneo={tour}")
    print("--- Cargando modelos de Miguel, Absalón y David ---\n")
    
    engine = GeneticEngine(p_crossover=cross, p_mutation=mut, tournament_size=tour)
    
    try:
        for estado in engine.ejecutar_evolucion(dataset, generaciones=gens, tam_poblacion=pop):
            if "final" in estado:
                print(f"\n[ÉXITO] Evolución completada con éxito en {estado['tiempo']}s.")
                if "mse_test" in estado:
                    print(f"[RESULTADO] MSE de Prueba (30% invisible): {estado['mse_test']:.6f}")
                break
            else:
                formula_str = estado['formula']
                if len(formula_str) > 80:
                    formula_str = formula_str[:77] + "..."
                print(f"[Generación {estado['gen']}] MSE: {estado['mse']:.6f} | Mejor fórmula: {formula_str}")
    except Exception as e:
        print(f"\n[ERROR] Error durante la evolución: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GP Engine - Unidad 4")
    parser.add_argument("--data", type=str, help="Nombre del dataset (ej: housing)")
    parser.add_argument("--gens", type=int, default=50, help="Número de generaciones")
    parser.add_argument("--pop", type=int, default=500, help="Tamaño de la población")
    parser.add_argument("--cross", type=float, default=0.9, help="Probabilidad de cruce")
    parser.add_argument("--mut", type=float, default=0.1, help="Probabilidad de mutación")
    parser.add_argument("--tour", type=int, default=7, help="Tamaño de torneo")
    
    args = parser.parse_args()

    if args.data:
        modo_consola(args.data, args.gens, args.pop, args.cross, args.mut, args.tour)
    else:
        lanzar_web()