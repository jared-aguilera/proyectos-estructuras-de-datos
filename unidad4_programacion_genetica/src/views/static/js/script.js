document.addEventListener('DOMContentLoaded', () => {
    const btnRun = document.getElementById('btn-run');
    const btnGP = document.getElementById('btn-gplearn');
    const datasetSelect = document.getElementById('dataset');
    const terminal = document.getElementById('terminal');
    const formulaDiv = document.getElementById('formula');
    const mseSpan = document.getElementById('mse-val');
    const genSpan = document.getElementById('gen-val');
    const timeSpan = document.getElementById('time-val');
    const fileUpload = document.getElementById('file-upload');


    class ASTViewer {
        constructor(canvasId) {
            this.canvas = document.getElementById(canvasId);
            this.ctx = this.canvas.getContext('2d');
            this.currentAST = null;
            this.cameraX = this.canvas.width / 2;
            this.cameraY = 50;
            this.zoomScale = 1.0;
            this.isDragging = false;
            this.startDragX = 0;
            this.startDragY = 0;

            this.canvas.addEventListener('mousedown', (e) => {
                this.isDragging = true;
                this.startDragX = e.clientX - this.cameraX;
                this.startDragY = e.clientY - this.cameraY;
            });

            this.canvas.addEventListener('mousemove', (e) => {
                if (this.isDragging) {
                    this.cameraX = e.clientX - this.startDragX;
                    this.cameraY = e.clientY - this.startDragY;
                    this.drawAST();
                }
            });

            this.canvas.addEventListener('mouseup', () => this.isDragging = false);
            this.canvas.addEventListener('mouseleave', () => this.isDragging = false);
            
            this.canvas.addEventListener('wheel', (e) => {
                e.preventDefault(); // Prevent page scroll
                const zoomAmount = e.deltaY > 0 ? 0.9 : 1.1;
                this.zoomScale *= zoomAmount;
                this.drawAST();
            });
        }

        setTree(treeData) {
            this.currentAST = treeData;
            this.cameraX = this.canvas.width / 2;
            this.cameraY = 50;
            this.zoomScale = 1.0;
            this.drawAST();
        }

        getWidth(node) {
            if (!node) return 0;
            if (!node.izq && !node.der) return 60; // leaf width
            let w = 0;
            if (node.izq) w += this.getWidth(node.izq);
            if (node.der) w += this.getWidth(node.der);
            return w;
        }

        getStyle(valor) {
            if (['+', '-', '*', '/'].includes(valor)) return {col: "#34495e", txt: valor};
            if (['sin', 'cos', 'log', 'sqrt', 'exp'].includes(valor)) return {col: "#3498db", txt: valor};
            if (valor.startsWith('X')) return {col: "#e67e22", txt: valor};
            const num = parseFloat(valor);
            return {col: "#9b59b6", txt: !isNaN(num) ? num.toFixed(2) : valor};
        }

        drawNode(node, x, y) {
            if (!node) return;
            const distY = 80;
            const yChild = y + distY;
            let totalWidth = this.getWidth(node);
            let xCursor = x - (totalWidth / 2);

            if (node.izq) {
                let wIzq = this.getWidth(node.izq);
                let xChild = xCursor + (wIzq / 2);
                this.ctx.beginPath();
                this.ctx.moveTo(x, y);
                this.ctx.lineTo(xChild, yChild);
                this.ctx.strokeStyle = "#555";
                this.ctx.lineWidth = 2;
                this.ctx.stroke();
                this.drawNode(node.izq, xChild, yChild);
                xCursor += wIzq;
            }
            if (node.der) {
                let wDer = this.getWidth(node.der);
                let xChild = xCursor + (wDer / 2);
                this.ctx.beginPath();
                this.ctx.moveTo(x, y);
                this.ctx.lineTo(xChild, yChild);
                this.ctx.strokeStyle = "#555";
                this.ctx.lineWidth = 2;
                this.ctx.stroke();
                this.drawNode(node.der, xChild, yChild);
            }

            const style = this.getStyle(node.valor);
            const r = 25;
            this.ctx.beginPath();
            this.ctx.arc(x, y, r, 0, 2 * Math.PI);
            this.ctx.fillStyle = style.col;
            this.ctx.fill();
            this.ctx.lineWidth = 2;
            this.ctx.strokeStyle = "white";
            this.ctx.stroke();

            this.ctx.fillStyle = "white";
            this.ctx.font = "bold 12px Roboto, sans-serif";
            this.ctx.textAlign = "center";
            this.ctx.textBaseline = "middle";
            this.ctx.fillText(style.txt, x, y);
        }

        drawAST() {
            this.ctx.save();
            this.ctx.setTransform(1, 0, 0, 1, 0, 0);
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            this.ctx.restore();

            if (this.currentAST) {
                this.ctx.save();
                this.ctx.translate(this.canvas.width / 2, this.canvas.height / 2);
                this.ctx.scale(this.zoomScale, this.zoomScale);
                this.ctx.translate(-this.canvas.width / 2, -this.canvas.height / 2);

                this.drawNode(this.currentAST, this.cameraX, this.cameraY);
                this.ctx.restore();
            }
        }
    }

    const viewerPropio = new ASTViewer('ast-canvas');
    const viewerGP = new ASTViewer('ast-canvas-gp');

    // Inicializar gráfica de convergencia vacía
    const ctxChart = document.getElementById('convergence-chart').getContext('2d');
    let convergenceChart = new Chart(ctxChart, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Error (MSE)',
                data: [],
                borderColor: '#1abc9c',
                backgroundColor: 'rgba(26, 188, 156, 0.2)',
                borderWidth: 2,
                pointRadius: 3,
                pointBackgroundColor: '#16a085',
                fill: true,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: { display: true, text: 'Generación', color: '#ccc' },
                    ticks: { color: '#aaa' },
                    grid: { color: '#333' }
                },
                y: {
                    title: { display: true, text: 'MSE', color: '#ccc' },
                    ticks: { color: '#aaa' },
                    grid: { color: '#333' }
                }
            },
            plugins: {
                legend: { labels: { color: '#eee' } }
            }
        }
    });

    // Evento para cambiar etiquetas segun la metrica
    document.getElementById('hp-metric').addEventListener('change', function() {
        const label = this.options[this.selectedIndex].text.split(' ')[0];
        document.querySelectorAll('.metric-label').forEach(el => el.innerText = label);
        document.querySelectorAll('.metric-label-gp').forEach(el => el.innerText = label);
        
        convergenceChart.data.datasets[0].label = `Error (${label})`;
        convergenceChart.options.scales.y.title.text = label;
        convergenceChart.update();
        
        convergenceChartGP.data.datasets[0].label = `Error GPLearn (${label})`;
        convergenceChartGP.options.scales.y.title.text = label;
        convergenceChartGP.update();
    });

    const ctxChartGP = document.getElementById('convergence-chart-gp').getContext('2d');
    let convergenceChartGP = new Chart(ctxChartGP, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Error GPLearn (MSE)',
                data: [],
                borderColor: '#9b59b6',
                backgroundColor: 'rgba(155, 89, 182, 0.2)',
                borderWidth: 2,
                pointRadius: 3,
                pointBackgroundColor: '#8e44ad',
                fill: true,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: { display: true, text: 'Generación', color: '#ccc' },
                    ticks: { color: '#aaa' },
                    grid: { color: '#333' }
                },
                y: {
                    title: { display: true, text: 'MSE', color: '#ccc' },
                    ticks: { color: '#aaa' },
                    grid: { color: '#333' }
                }
            },
            plugins: {
                legend: { labels: { color: '#eee' } }
            }
        }
    });

    datasetSelect.addEventListener('change', () => {
        if (datasetSelect.value === 'custom') {
            fileUpload.style.display = 'block';
        } else {
            fileUpload.style.display = 'none';
        }
    });

    // Forzar que los inputs respeten min y max al perder el foco
    document.querySelectorAll('.input-group input').forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value === '') return;
            let val = parseFloat(this.value);
            let min = parseFloat(this.min);
            let max = parseFloat(this.max);
            
            if (!isNaN(min) && val < min) this.value = min;
            if (!isNaN(max) && val > max) this.value = max;
        });
    });

    function logToTerminal(message, type = 'info') {
        const line = document.createElement('div');
        line.className = `log-${type}`;
        line.innerText = `[${new Date().toLocaleTimeString()}] ${message}`;
        terminal.appendChild(line);
        terminal.scrollTop = terminal.scrollHeight; 
    }

    function getHyperparams() {
        const gensStr = document.getElementById('hp-gens').value;
        const popStr = document.getElementById('hp-pop').value;
        const crossStr = document.getElementById('hp-cross').value;
        const mutStr = document.getElementById('hp-mut').value;
        const tourStr = document.getElementById('hp-tour').value;
        const initDepthStr = document.getElementById('hp-init-depth').value;
        const maxDepthStr = document.getElementById('hp-max-depth').value;
        const metric = document.getElementById('hp-metric').value;
        
        const gens = gensStr !== '' ? parseInt(gensStr) : 50;
        const pop = popStr !== '' ? parseInt(popStr) : 500;
        const cross = crossStr !== '' ? parseFloat(crossStr) : 0.9;
        const mut = mutStr !== '' ? parseFloat(mutStr) : 0.1;
        const tour = tourStr !== '' ? parseInt(tourStr) : 7;
        const initDepth = initDepthStr !== '' ? parseInt(initDepthStr) : 4;
        const maxDepth = maxDepthStr !== '' ? parseInt(maxDepthStr) : 17;

        if (gens <= 0 || pop <= 0) {
            logToTerminal('Error: Generaciones y Población deben ser mayores a 0.', 'error');
            return null;
        }
        if (cross < 0 || cross > 1 || mut < 0 || mut > 1) {
            logToTerminal('Error: Las probabilidades deben estar entre 0.0 y 1.0.', 'error');
            return null;
        }
        if (tour > pop || tour < 2) {
            logToTerminal('Error: El tamaño de torneo debe ser al menos 2 y no mayor a la población.', 'error');
            return null;
        }
        if (initDepth >= maxDepth) {
            logToTerminal('Error: La profundidad inicial debe ser menor a la profundidad máxima.', 'error');
            return null;
        }

        return `?gens=${gens}&pop=${pop}&cross=${cross}&mut=${mut}&tour=${tour}&init_depth=${initDepth}&max_depth=${maxDepth}&metric=${metric}`;
    }

    async function handleUpload() {
        if (datasetSelect.value !== 'custom') return datasetSelect.value;
        if (!fileUpload.files.length) {
            logToTerminal('Error: Por favor selecciona un archivo (.csv o .data) para subir.', 'error');
            return null;
        }
        
        const file = fileUpload.files[0];
        const formData = new FormData();
        formData.append('file', file);
        
        logToTerminal(`Subiendo dataset ${file.name}...`, 'info');
        
        try {
            const response = await fetch('/upload-dataset', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            if (data.status === 'success') {
                return data.dataset_name;
            } else {
                logToTerminal(`Error al subir dataset: ${data.message}`, 'error');
                return null;
            }
        } catch (error) {
            logToTerminal('Error de conexión al subir el dataset.', 'error');
            return null;
        }
    }

    btnRun.addEventListener('click', async () => {
        const dataset = await handleUpload();
        if (!dataset) return;
        
        const params = getHyperparams();
        if (!params) return; // Validation failed

        const gensStr = document.getElementById('hp-gens').value;
        document.getElementById('gen-total').innerText = gensStr !== '' ? parseInt(gensStr) : 50;

        document.getElementById('ast-container').style.display = 'none';
        document.getElementById('chart-container').style.display = 'block';
        
        btnRun.disabled = true;
        terminal.innerHTML = '';
        timeSpan.innerText = '--';
        document.getElementById('mse-test-val').innerText = '--';
        
        // Reset chart data
        convergenceChart.data.labels = [];
        convergenceChart.data.datasets[0].data = [];
        convergenceChart.update();

        logToTerminal(`Iniciando evolución para ${dataset}...`, 'info');

        const eventSource = new EventSource(`/run-evolution/${dataset}${params}`);

        eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            if (data.final) {
                timeSpan.innerText = data.tiempo;
                if (data.mse_test !== undefined) {
                    document.getElementById('mse-test-val').innerText = data.mse_test.toFixed(4);
                    logToTerminal(`--- EVALUACIÓN FINAL ---`, 'info');
                    logToTerminal(`MSE Prueba (30% invisible) = ${data.mse_test.toFixed(4)}`, 'success');
                } else {
                    logToTerminal(`Evolución completada con éxito en ${data.tiempo}s.`, 'info');
                }
                
                if (data.arbol) {
                    viewerPropio.setTree(data.arbol);
                    document.getElementById('ast-container').style.display = 'block';
                }

                eventSource.close();
                btnRun.disabled = false;
                return;
            }

            genSpan.innerText = data.gen + 1;
            mseSpan.innerText = data.mse.toFixed(4);
            formulaDiv.innerText = data.formula;
            
            // Actualizar gráfica animada
            convergenceChart.data.labels.push(data.gen);
            convergenceChart.data.datasets[0].data.push(data.mse);
            convergenceChart.update();
            
            const metricLabel = document.getElementById('hp-metric').options[document.getElementById('hp-metric').selectedIndex].text.split(' ')[0];
            logToTerminal(`Generación ${data.gen}: ${metricLabel} = ${data.mse.toFixed(4)}`, 'success');
        };

        eventSource.onerror = () => {
            logToTerminal('Error en la conexión con el motor.', 'error');
            eventSource.close();
            btnRun.disabled = false;
        };
    });

    btnGP.addEventListener('click', async () => {
        const dataset = await handleUpload();
        if (!dataset) return;
        
        const gpCard = document.getElementById('gplearn-card');
        const params = getHyperparams();
        if (!params) return; // Validation failed
        
        document.getElementById('ast-container-gp').style.display = 'none';
        document.getElementById('chart-container-gp').style.display = 'block';
        btnGP.disabled = true;
        logToTerminal('Ejecutando gplearn para comparativa...', 'info');
        
        try {
            const response = await fetch(`/run-gplearn/${dataset}${params}`);
            const data = await response.json();
            
            if (data.status === 'success') {
                gpCard.classList.remove('hidden');
                
                document.getElementById('gp-formula').innerText = data.formula;
                document.getElementById('gp-mse-train').innerText = data.mse_train.toFixed(6);
                document.getElementById('gp-mse-test').innerText = data.mse_test.toFixed(6);
                document.getElementById('gp-time').innerText = data.tiempo;
                
                if (data.arbol) {
                    viewerGP.setTree(data.arbol);
                    document.getElementById('ast-container-gp').style.display = 'block';
                }
                
                if (data.historial_mse) {
                    convergenceChartGP.data.labels = data.historial_mse.map((_, i) => i);
                    convergenceChartGP.data.datasets[0].data = data.historial_mse;
                    convergenceChartGP.update();
                }
                
                logToTerminal(`GPLearn finalizó. Tiempo: ${data.tiempo}s`, 'info');
            } else {
                logToTerminal(`Error de gplearn: ${data.message}`, 'error');
            }
        } catch (error) {
            logToTerminal('No se pudo conectar con el servidor para gplearn.', 'error');
        } finally {
            btnGP.disabled = false;
        }
    });
});