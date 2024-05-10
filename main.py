from flask import Flask, jsonify, request
import json, requests
from api_gemini import genai

app = Flask(__name__)

model = genai.GenerativeModel(model_name='gemini-1.5-pro-latest')
chat = model.start_chat(history=[])

@app.route("/businesschat", methods=['GET', 'POST'])
def responder():
    try:
        data = request.data
        dados = json.loads(data.decode('utf-8'))
        mensagem = dados.get('mensagem')

        if mensagem is None:
            return jsonify({"Erro: 'mensagem' não encontrada nos dados."})
        else:
            prompt = f'Gere uma frase'
            response = chat.send_message(prompt)
            return jsonify({'resposta': response.text})
    except requests.exceptions.RequestException as e:
        return jsonify({"Erro": "Erro ao obter dados da API."})
    except json.JSONDecodeError:
        return jsonify({"Erro": "Formato JSON inválido."})
    except Exception as e:
        return jsonify({"Erro": str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
