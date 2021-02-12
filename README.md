# Rasa Open Source


Rasa é uma estrutura de aprendizado de máquina de código aberto para automatizar conversas baseadas em texto e voz. Com o Rasa, você pode criar assistentes contextuais em:

* **Facebook Messenger**
* **Slack**
* **Google Hangouts**
* **Webex Teams**
* **Microsoft Bot Framework**
* **Microsoft teams**
* **Rocket.Chat**
* **Mattermost**
* **Telegram**
* **Twilio**
* **Seus próprios canais de conversação personalizados**

ou assistentes de voz:

* **Alexa Skills**
* **Google Home Actions**

O Rasa ajuda a criar assistentes contextuais capazes de ter conversas em camadas com muitas idas e vindas. Para que um humano tenha uma troca significativa com um assistente contextual, o assistente precisa ser capaz de usar o contexto para desenvolver coisas que foram discutidas anteriormente - o Rasa permite que você crie assistentes que podem fazer isso de uma forma escalável.

---
- **O que o Rasa faz? 🤔**
  [Confira nosso site](https://rasa.com/)

- **Eu sou novo no rasa  😄**
  [Começe a usar o rasa](https://rasa.com/docs/getting-started/)

- **Eu gostaria de ler a documentação detalhada 🤓**
  [Leia os Documentos](https://rasa.com/docs/)

- **Estou pronto para instalar o Rasa 🚀**
  [Instalação](https://rasa.com/docs/rasa/user-guide/installation/)

- **Eu quero aprender como usar o Rasa 🚀**
  [Tutorial](https://rasa.com/docs/rasa/user-guide/rasa-tutorial/)

- **Eu tenho uma pergunta ❓**
  [Rasa Community Forum](https://forum.rasa.com/)

---
## Onde obter ajuda

Existe uma extensa documentação no [Rasa Docs](https://rasa.com/docs/rasa). Certifique-se de selecionar a versão correta para que possa consultar os documentos da versão que instalou.

## Projeto POC - QABOT - VIVO

Projeto para ajudar a registrar as ocorrências referentes à defeitos de clientes da operadora.

## Como Obter o Repositório

Acesso Interno aos colaboradores da Compasso

## Como Rodar o Projeto

Importante! Para executar o projeto é necessário ter o Rasa, docker e o Python (3.6 ou 3.7 ou 3.8) instalado na sua máquina.

No docker execute o comando **docker run -d -p 8000:8000 rasa/duckling** para rodar o serviço do Duckling em segundo plano, que é utilizado como extrator de entidades.

Além disso, também é necessário ter o **Spacy** instalado na sua máquina. Para instalar, execute os comandos:

* pip install -U spacy //para instalar o Spacy
* python -m spacy download pt_core_news_lg //para baixar o modelo em português do Spacy

* Para executar o projeto execute os comandos:

* Abra um terminal no diretório do projeto e execute o comando **rasa train**, para treinar um novo modelo;
* Após isso, execute o comando **rasa run actions**, para iniciar o servidor de custom actions;
* Abra outro terminal no diretório do projeto e execute o comando **rasa shell**, para iniciar a conversa com o chatbot no terminal

## Principais Branchs

* master(Produção)
* develop
* TR(Desenvolvimento)

## Tags do Projeto

* v0.1.0 // Sprint 1
* v0.2.0 // Sprint 2
* v0.3.0 // Sprint 3
* v0.4.0 // Sprint 4

## Principais Contribuidores

---
- Responsável Pelo Desenvolvimento do Código

- **natanael.silva@compasso.com.br**
- **vanessa.silva@compasso.com.br**
- **lucas.marca@compasso.com.br**
- **henry.pereira@compasso.com.br**
- **caina.rodrigues@compasso.com.br**

- Responsável Por UX/UI

- **alberto.silva@compasso.com.br**

- Responsável por QA

- **marcelo.reis@compasso.com.br**

- Scrum Master do Projeto

- **boris.garafulic@compasso.com.br**

- Líder Técnico

- **daniel.muller@compasso.com.br**

---

## Regras de Boas Práticas para o Projeto

flake instalação:

* pip install flake8
* flake8 --install-hook git
* git config --bool flake8.strict true