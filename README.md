## Projeto: Plataforma de conteúdo sobre negócios estilo portal com Chatbot e recomendação Just in time
**Projeto criado para o desafio 2ª Imersão IA - Alura + Google**<br>

A plataforma tem o propósito de oferecer séries de conteúdo no formato streaming no nicho de negócios proporcionando uma experiência amigável ao usuário. Ainda oferece um Chatbot inteligente especialista em consultoria de negócios para empresas brasileiras com capacidade para orientar, informar, tirar dúvidas sobre os conteúdos da plataforma e o que mais o usuário precisar.

![Businessflix](https://github.com/joselinosantos/businessflix-backend/blob/master/businessflix.png)

### Tecnologias
1. Google Gemini, Google IA Studio - Poderosa ferramenta de LLM: [Site do Gemini](https://gemini.google.com/?hl=en-GB)
2. Flask - Framework web leve e rápido em Python: [Site do framework](https://flask.palletsprojects.com/en/3.0.x/)
3. Trio da alegria da Web: HTML, CSS, Javascript. [Artigo da Alura](https://www.alura.com.br/artigos/html-css-e-js-definicoes)

### Diagrama
![Diagrama](https://github.com/joselinosantos/businessflix-backend/blob/master/imagens/diagrama.png)

### Desenvolvimento
1. Testes com a API do Gemini para verificar o comportamento na aplicação e contexto do projeto nos models pro e 1.5-pro-latest
2. Preparação da API com a utilização do dotenv (uma forma de gerenciar API_KEYS com mais segurança)
   [Dotenv passo a passo](https://www.dotenv.org/docs/quickstart.html)
4. Primeiro endpoint (/businesschat)
   * É o endpoint padrão do Chatbot que recebe os dados das requisições, onde foi montado o prompt e retorna a resposta em JSON
   * O modelo escolhido foi o <b>1.5-pro-latest</b> por apresentar um excelente resultado nos testes ao tratar adequadamente apenas sobre o assunto definido nas regras do prompt
   * Possui tratamento de erros para formato JSON errado, erros de requests e outros genéricos
5. Endpoint /history apenas para testar o histórico do chat
6. Endpoint /recomendacoes
   * Faz uma requisição a uma API externa(que seria do banco de dados) para que o Gemini tenha o contexto da plataforma ao recomendar itens
   * Alimentado pelos dados do próprio Chat enquanto o usuário interage (para isso recebe o histórico com chat.history)
   * Ao realizar testes com o modelo 1.5-pro-latest as respostas variaram bastante, portanto foi usada a 1.5-pro com temperatura=0 com a finalidade de retornar apenas o JSON formatado adequadamente para ser retornado como resposta
   * O prompt foi criado com auxílio da própria ferramenta e apresentou bons resultados. Ele basicamente recebe a base de dados da plataforma e o histórico do chat e tem que recomendar os 4 itens com maior probabilidade de interesse do usuário. Dessa forma a plataforma se torna muito mais dinâmica, embora requeira aprimoramentos.

### Execução do backend
**Abra o terminal e acesse a pasta do projeto**
1. Instale o virtualenv
```
    pip install virtualenv
```
2. Crie o ambiente virtual
```
    python -m venv .venv
```
3. Ative o ambiente virtual
```
    . .venv /bin/activate
```
4. Instale as bibliotecas necessárias
```
    pip install -r requirements.txt
```
5. Execute o arquivo main.py
```
    python main.py
```
6. Teste o endpoint businesschat.<br> Acesse o endereço http://127.0.0.1:5000/businesschat em alguma ferramenta para teste de API como: 
  * [Insomnia](https://insomnia.rest/download)
  * [Postman](https://www.postman.com/)

No caso estou usando Insomnia para fazer uma requisição do tipo GET.

![Teste endpoint businesschat](https://github.com/joselinosantos/businessflix-backend/blob/master/imagens/api_businesschat.png)

Observe que o corpo do JSON possui a solicitação que será incluída dentro do prompt.

7. Após algumas interações com o Chat teste o endpoint de recomendações com o endereço: http://127.0.0.1:5000/recomendacoes
![Teste endpoint recomendacoes](https://github.com/joselinosantos/businessflix-backend/blob/master/imagens/api_recomendacoes.png)

### Front end
Por uma questão de boa prática e organização, todo o front end é separado e está em outro repositório. <br>
São apenas arquivos HTML, CSS e JavaScript sendo o JS fundamental para listagem dos dados e as requisições à API<br>
Para testar acesse o repositório: [Front end do projeto](https://github.com/joselinosantos/businessflix-frontend.git)

### Testes realizados
1 Solicitação de conteúdos de assuntos não relacionados com o nicho como física quântica, por exemplo
2 Erros ortográficos diversos e propositais
3 Tentativa de sobrecarga do Chat com múltiplas mensagens
4 Inserir um texto Loren ipsum sem sentido com múltiplas cópias ao mesmo tempo 

### Limitações
1 Não foram tratados todos os erros possíveis
2 Na recomendação requisições são realizadas durante as interações o que não é performático (deverá ser melhorado)
3 O Chat possui contexto limitado ao exemplo incluído no prompt

### Features Futuras
1 Analisador de negócios com IA
2 Ferramentas para negócios com IA
3 Trilha personalizada por IA para o usuário
