from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

# Configuração da API do Gemini
genai.configure(api_key="AIzaSyCxfo9OjH_0lS7GOvwbkA23X3CcbFoR3vk")

# Inicialização do Flask
app = Flask(__name__)

# Pesos para o cálculo da média ponderada
PESOS = {
    "linguagens": 1,
    "humanas": 2,
    "matematica": 3,
    "ciencias": 2,
    "redacao": 2
}

def calcular_soma_media_ponderada(notas):
    """Calcula a soma e a média ponderada das notas."""
    soma = sum(notas.values())
    media_ponderada = sum(notas[nota] * PESOS[nota] for nota in notas) / sum(PESOS.values())
    return soma, media_ponderada

@app.route("/")
def home():
    """Página inicial para input do usuário."""
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    """Processa os dados enviados pelo frontend, calcula a média e consulta a API do Gemini."""
    try:
        # Receber dados do frontend
        data = request.get_json()
        if not data:
            return jsonify({"error": "Nenhum dado recebido"}), 400

        notas = {
            "linguagens": float(data.get("linguagens", 0)),
            "humanas": float(data.get("humanas", 0)),
            "matematica": float(data.get("matematica", 0)),
            "ciencias": float(data.get("ciencias", 0)),
            "redacao": float(data.get("redacao", 0)),
        }
        curso = data.get("curso", "")
        regiao = data.get("regiao", "")
        estado = data.get("estado", "")
        cota = data.get("cota", "")

        # Calcular soma e média ponderada
        soma, media_ponderada = calcular_soma_media_ponderada(notas)

        # Consultar a API do Gemini
        model = genai.GenerativeModel("gemini-pro")
        prompt = (f"Um candidato com média ponderada de {media_ponderada:.2f}, "
                  f"do estado {estado}, com cota '{cota}', deseja cursar {curso} na região {regiao}. "
                  "Quais faculdades na região oferecem esse curso? "
                  "Se a nota não for suficiente, sugira alternativas de cursos ou faculdades para o candidato.")
        response = model.generate_content(prompt)

        # Retornar a resposta da API e informações adicionais
        resultado = {
            "soma": soma,
            "media_ponderada": media_ponderada,
            "recommendations": response.text
        }
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)  