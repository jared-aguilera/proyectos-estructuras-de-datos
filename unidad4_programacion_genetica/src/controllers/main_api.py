from fastapi import FastAPI, Request, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, StreamingResponse
import os
import json
import time
import asyncio
import shutil
from src.models.engine import GeneticEngine
from gplearn.genetic import SymbolicRegressor
from src.utils.data_loader import DataLoader
from sklearn.model_selection import train_test_split
import numpy as np

app = FastAPI()

root_path = os.path.dirname(os.path.dirname(__file__))
static_path = os.path.join(root_path, "views", "static")

app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/", response_class=HTMLResponse)
async def home():
    index_path = os.path.join(static_path, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()

@app.post("/upload-dataset")
async def upload_dataset(file: UploadFile = File(...)):
    try:
        data_dir = os.path.join(root_path, "..", "data")
        os.makedirs(data_dir, exist_ok=True)
        file_path = os.path.join(data_dir, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        dataset_name = os.path.splitext(file.filename)[0]
        return {"status": "success", "dataset_name": dataset_name}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/run-evolution/{dataset}")
async def start_evolution(dataset: str, gens: int = 50, pop: int = 500, cross: float = 0.9, mut: float = 0.1, tour: int = 7, init_depth: int = 4, max_depth: int = 17, metric: str = "mse"):
    """Endpoint con streaming para ver la terminal en vivo"""
    engine = GeneticEngine(p_crossover=cross, p_mutation=mut, tournament_size=tour, max_depth=max_depth)
    
    def generate():
        for data in engine.ejecutar_evolucion(dataset, generaciones=gens, tam_poblacion=pop, max_depth_init=init_depth, metric=metric):
            # Formato SSE: 'data: {json}\n\n'
            yield f"data: {json.dumps(data)}\n\n"
            time.sleep(0.01) 
            
    return StreamingResponse(generate(), media_type="text/event-stream")

@app.get("/run-gplearn/{dataset}")
async def run_gplearn(dataset: str, gens: int = 50, pop: int = 500, cross: float = 0.9, mut: float = 0.1, tour: int = 7, init_depth: int = 4, max_depth: int = 17, metric: str = "mse"):
    """Comparativa oficial con la libreria gplearn"""
    try:
        X, y = DataLoader.cargar_dataset(dataset)
        # division 70-30 pura aleatoria con sklearn
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
        
        start_time = time.time()
        
        # En gplearn las prob. deben sumar <= 1.0
        suma_prob = cross + mut
        p_point = round(max(0.0, 1.0 - suma_prob), 2)
        if suma_prob > 1.0:
            cross = 0.9
            mut = 0.1
            p_point = 0.0

        # Mapeo de metricas para gplearn
        gp_metric = "mse"
        if metric == "mae": gp_metric = "mean absolute error"
        elif metric == "rmse": gp_metric = "rmse"
        elif metric == "mape": gp_metric = "mape" # Nota: gplearn soporta mape

        est = SymbolicRegressor(population_size=pop,
                               generations=gens,
                               stopping_criteria=0.01,
                               tournament_size=tour,
                               init_depth=(2, init_depth),
                               p_crossover=cross, 
                               p_subtree_mutation=mut,
                               p_hoist_mutation=0,
                               p_point_mutation=p_point,
                               max_samples=1.0,
                               verbose=0,
                               metric=gp_metric,
                               random_state=None)
        
        est.fit(X_train, y_train)
        end_time = time.time()
        
        # Traducir string de gplearn a AST JSON
        def parse_gplearn_string(s):
            def parse_expr(s, idx):
                token = ""
                while idx < len(s) and s[idx] not in '(), ':
                    token += s[idx]
                    idx += 1
                if token in ['add', 'sub', 'mul', 'div', 'sin', 'cos', 'log', 'sqrt', 'exp']:
                    op = {'add':'+', 'sub':'-', 'mul':'*', 'div':'/'}.get(token, token)
                    node = {"valor": op}
                    if idx < len(s) and s[idx] == '(':
                        idx += 1 # skip '('
                        node["izq"], idx = parse_expr(s, idx)
                        while idx < len(s) and s[idx] in ' ,':
                            idx += 1 # skip ', '
                        if token not in ['sin', 'cos', 'log', 'sqrt', 'exp']: # binarios
                            node["der"], idx = parse_expr(s, idx)
                        while idx < len(s) and s[idx] in ' ,':
                            idx += 1
                        if idx < len(s) and s[idx] == ')':
                            idx += 1
                    return node, idx
                else:
                    return {"valor": token}, idx
            
            try:
                return parse_expr(s, 0)[0]
            except:
                return None

        formula_str = str(est._program)
        
        # Calculo de MSE de Prueba manualmente (numpy puro)
        y_pred = est.predict(X_test)
        mse_test_val = np.mean(np.square(y_test - y_pred))
        
        return {
            "status": "success",
            "mse_train": float(est._program.raw_fitness_),
            "mse_test": float(mse_test_val),
            "formula": formula_str,
            "arbol": parse_gplearn_string(formula_str),
            "tiempo": round(end_time - start_time, 4),
            "historial_mse": est.run_details_['best_fitness']
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}