let currentStep = 1;

function showStep(step) {
    document.querySelectorAll('.step').forEach((stepElement, index) => {
        stepElement.classList.toggle('active', index === step - 1);
    });
}

function nextStep() {
    if (currentStep < 3) {
        if (currentStep === 2) {
            enviarDados();
        }
        currentStep++;
        showStep(currentStep);
    }
}

function prevStep() {
    if (currentStep > 1) {
        currentStep--;
        showStep(currentStep);
    }
}

function enviarDados() {
    const dados = {
        matematica: parseFloat(document.getElementById('matematica').value || 0),
        humanas: parseFloat(document.getElementById('humanas').value || 0),
        natureza: parseFloat(document.getElementById('natureza').value || 0),
        linguagens: parseFloat(document.getElementById('linguagens').value || 0),
        redacao: parseFloat(document.getElementById('redacao').value || 0),
        estado: document.getElementById('estado').value || "",
        cidade: document.getElementById('cidade').value || "",
        escolaridade: document.getElementById('escolaridade').value || "",
        curso: document.getElementById('curso').value || "",
        cotas: document.getElementById('cotas').value || "",
    };

    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dados)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(`Erro: ${data.error}`);
        } else {
            const resultadoElement = document.getElementById('resultado');
            resultadoElement.textContent = `Soma das notas: ${data.soma}, Média ponderada: ${data.media_ponderada.toFixed(2)}. Recomendações: ${data.recommendations}`;
        }
    })
    .catch(error => {
        console.error('Erro ao enviar dados:', error);
        alert('Erro ao processar a solicitação.');
    });
}