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


@app.route("/history")
def historico():
    try:
        historico = chat.history

        if historico:
            return jsonify({'resposta': chat.history})
        else:
            return jsonify({'resposta': 'Sem dados no histórico'})
    except requests.exceptions.RequestException as e:
        return jsonify({"Erro": "Erro ao obter dados da API."})
    except json.JSONDecodeError:
        return jsonify({"Erro": "Formato JSON inválido."})
    except Exception as e:
        return jsonify({"Erro": str(e)})


@app.route("/recomendacoes")
def recomendar():
    try:
        API_TITULOS = 'http://localhost:3000/series'
        
        response = requests.get(API_TITULOS)
        response.raise_for_status()
        series_data = response.json()
        historico = chat.history

        if historico:
            generation_config = {
                "temperature": 0,
            }

            model = genai.GenerativeModel(model_name='gemini-pro', generation_config=generation_config)

            prompt = f"""Você é um sistema de recomendação de conteúdo especializado em séries de negócios. \
            Analise o histórico de conversa a seguir: \
            {historico} 
            Com base nas informações extraídas da conversa, identifique e recomende apenas as 4 séries da lista a seguir que têm maior probabilidade de interessar ao usuário. \
            Priorize séries que estejam diretamente relacionadas aos tópicos e interesses demonstrados na conversa. \
            Formato da resposta (JSON): id, titulo, autor, capa \
            Dados dos títulos: {series_data}"""

            response_recomendacao = model.generate_content(prompt)

            return jsonify({'resposta': response_recomendacao.text})
        else:
            return jsonify({'resposta': series_data})
    except json.JSONDecodeError:
        return jsonify({"Erro: Formato JSON inválido."})
    except Exception as e:
        return jsonify({"Erro": str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
