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
            return jsonify({"Erro": "'mensagem' não encontrada nos dados."})
        else:
            API_TITULOS = 'http://localhost:3000/series'
            response = requests.get(API_TITULOS)
            
            response.raise_for_status()

            series_data = response.json()

            # Formatação dos dados das séries
            titulos_series = [serie['titulo'] for serie in series_data]
            lista_titulos = '\n'.join(titulos_series)

            prompt = f'Você é um consultor empresarial especialista em negócios das empresas brasileiras. Seu nome é Businesschat \
            Contexto: Você faz parte da plataforma de estudos sobre negócios Businessflix que possui os seguintes títulos(séries): \
            {lista_titulos} \
            Sendo assim responda o que é solicitado a seguir de forma direta. Não responda questões que não sejam do contexto empresarial. \
            Se a solicitação não for sobre o contexto empresarial e da plataforma responda educadamente que só pode ajudar com questões empresariais(sinta-se livre para variar as respostas)." \
            A solicitação é: {mensagem}'

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
