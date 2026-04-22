document.addEventListener('DOMContentLoaded', () => {
    const btnRun = document.getElementById('btn-run');
    const btnGP = document.getElementById('btn-gplearn');
    const datasetSelect = document.getElementById('dataset');
    const terminal = document.getElementById('terminal');
    const formulaDiv = document.getElementById('formula');
    const mseSpan = document.getElementById('mse-val');
    const genSpan = document.getElementById('gen-val');
    const timeSpan = document.getElementById('time-val');

    function logToTerminal(message, type = 'info') {
        const line = document.createElement('div');
        line.className = `log-${type}`;
        line.innerText = `[${new Date().toLocaleTimeString()}] ${message}`;
        terminal.appendChild(line);
        terminal.scrollTop = terminal.scrollHeight; 
    }

    btnRun.addEventListener('click', () => {
        const dataset = datasetSelect.value;
        btnRun.disabled = true;
        terminal.innerHTML = '';
        timeSpan.innerText = '--';
        logToTerminal(`Iniciando evolución para ${dataset}...`, 'info');

        const eventSource = new EventSource(`/run-evolution/${dataset}`);

        eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            if (data.final) {
                timeSpan.innerText = data.tiempo;
                logToTerminal(`Evolución completada con éxito en ${data.tiempo}s.`, 'info');
                eventSource.close();
                btnRun.disabled = false;
                return;
            }

            genSpan.innerText = data.gen + 1;
            mseSpan.innerText = data.mse.toFixed(4);
            formulaDiv.innerText = data.formula;
            
            logToTerminal(`Generación ${data.gen}: MSE = ${data.mse.toFixed(4)}`, 'success');
        };

        eventSource.onerror = () => {
            logToTerminal('Error en la conexión con el motor.', 'error');
            eventSource.close();
            btnRun.disabled = false;
        };
    });

    btnGP.addEventListener('click', async () => {
        const dataset = datasetSelect.value;
        const gpCard = document.getElementById('gplearn-card');
        
        btnGP.disabled = true;
        logToTerminal('Ejecutando gplearn para comparativa...', 'info');
        
        try {
            const response = await fetch(`/run-gplearn/${dataset}`);
            const data = await response.json();
            
            if (data.status === 'success') {
                gpCard.classList.remove('hidden');
                
                document.getElementById('gp-formula').innerText = data.formula;
                document.getElementById('gp-mse').innerText = data.mse.toFixed(6);
                document.getElementById('gp-time').innerText = data.tiempo;
                
                logToTerminal(`gplearn terminó en ${data.tiempo}s con MSE ${data.mse.toFixed(4)}`, 'success');
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