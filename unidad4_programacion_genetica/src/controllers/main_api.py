from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, StreamingResponse
import os
import json
import time
import asyncio
from src.models.engine import GeneticEngine
from gplearn.genetic import SymbolicRegressor
from src.utils.data_loader import DataLoader

app = FastAPI()

root_path = os.path.dirname(os.path.dirname(__file__))
static_path = os.path.join(root_path, "views", "static")

app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/", response_class=HTMLResponse)
async def home():
    index_path = os.path.join(static_path, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/run-evolution/{dataset}")
async def start_evolution(dataset: str):
    """Endpoint con streaming para ver la terminal en vivo"""
    engine = GeneticEngine(p_crossover=0.9, p_mutation=0.1, tournament_size=7)
    
    def generate():
        for data in engine.ejecutar_evolucion(dataset):
            # Formato SSE: 'data: {json}\n\n'
            yield f"data: {json.dumps(data)}\n\n"
            time.sleep(0.01) # pequeño respiro para el stream
            
    return StreamingResponse(generate(), media_type="text/event-stream")

@app.get("/run-gplearn/{dataset}")
async def run_gplearn(dataset: str):
    """Comparativa oficial con la libreria gplearn"""
    try:
        X, y = DataLoader.cargar_dataset(dataset)
        
        start_time = time.time()
        
        # En gplearn las prob. deben sumar <= 1.0
        # Se baja p_crossover a 0.85 para que: 0.85 + 0.1 + 0.05 = 1.0
        est = SymbolicRegressor(population_size=500,
                               generations=50,
                               stopping_criteria=0.01,
                               p_crossover=0.85, 
                               p_subtree_mutation=0.1,
                               p_hoist_mutation=0,
                               p_point_mutation=0.05,
                               max_samples=1.0,
                               verbose=0,
                               random_state=None)
        
        est.fit(X, y)
        end_time = time.time()
        
        return {
            "status": "success",
            "mse": float(est._program.raw_fitness_),
            "formula": str(est._program),
            "tiempo": round(end_time - start_time, 4)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}