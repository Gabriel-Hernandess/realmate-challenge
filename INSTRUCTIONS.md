# Instructions para Executar o Projeto Realtime Chat

## Observações iniciais

* O frontend está bem básico, apenas para demonstrar o login com um possível painel de administração
* Utilizei o celery apenas para mostrar respectivo conhecimento, já que as tarefas do desafio são consideradas leves
* As rotas principais do desafio não exigem tokens de autenticação, para seguir o padrão proposto
* Fora as definições principais seguidas pelas instruções do desafio, tudo é apenas para demonstrar breve conhecimento

## Pré-requisitos

* Docker e Docker Compose instalados
* Node.js 20 (opcional, se quiser rodar frontend sem container)
* Python 3.13 (conforme .python-version no backend)

## 1. Rodando com Docker Compose

Na raiz do projeto (onde está o arquivo `docker-compose.yml`):

```
docker-compose up --build
```

Isso fará:

1. Criar o banco PostgreSQL (porta 5432)
2. Criar o Redis (porta 6379)
3. Rodar o backend Django (porta 80)
4. Rodar o Celery para tarefas assíncronas
5. Rodar o frontend React (porta 3000)

> Observação: O backend irá automaticamente criar um superuser admin com:
>
> * usuário: admin
> * email: [admin@example.com](mailto:admin@example.com)
> * senha: admin123

## 2. Backend

### 2.1 Rodar migrações manualmente (opcional)

Se precisar rodar manualmente:

```
docker-compose exec web sh -c "poetry run python manage.py makemigrations"
docker-compose exec web sh -c "poetry run python manage.py migrate"
```

### 2.2 Criar superuser manualmente (opcional)

```
docker-compose exec web sh -c "poetry run python manage.py createsuperuser"
```

### 2.3 Testar rotas

* Rotas **protegidas** (requer cookie JWT válido):

  * `GET http://localhost/conversations/`  → Listar todas as conversas
  * `POST http://localhost/auth/refresh-token/` → Refresh token
  * `POST http://localhost/auth/logout/`   → Logout
  * `GET http://localhost/conversations/<uuid:pk>/summaries/`   → Relatórios de conversa específica
* Rotas **públicas** (não exigem autenticação):

  * `POST http://localhost/webhook/`       → Receber eventos do webhook
  * `POST http://localhost/auth/login/`    → Login
  * `GET http://localhost/conversations/<uuid:pk>/` → Obter conversa específica do desafio

> Cookies:
>
> * `access_token` e `refresh_token` são armazenados nos cookies

## 3. Frontend

### 3.1 Rodar em container

```
docker-compose up --build frontend
```

* Frontend React estará disponível em `http://localhost:3000`

### 3.2 Rodar sem container

```
cd frontend/dashboard
npm install
npm start
```

> Observação: O frontend já está configurado para consumir o backend em `http://localhost` com cookies para autenticação.

## 4. Estrutura de Telas (Dashboard React)

* **Menu lateral**

  * Conversations → Lista de conversas, clicar abre modal estilo WhatsApp com mensagens e relatório diário da conversa
  * APIs → Mostra todas as rotas disponíveis
  * Logout → Pergunta se deseja sair e remove cookies

* **Modal de conversa**

  * Mensagens recebidas → alinhadas à esquerda
  * Mensagens enviadas → alinhadas à direita
  * Data abaixo da mensagem
  * Estilo “balões” como WhatsApp
  * Abaixo o relatório da conversa, gerado por IA
  * Botão de fechar no canto superior direito

## 5. Observações finais

* O backend e frontend possuem **Dockerfiles separados**:

  * Backend: `backend/Dockerfile`
  * Frontend: `frontend/dashboard/Dockerfile`
* Arquivo `.python-version` está em `backend/` e indica a versão Python usada
* Todos os scripts de inicialização e migrações já estão configurados no `docker-compose.yml`
* O Celery está configurado para processar tasks assíncronas (ex: processamento de webhooks)
* Para alterações no frontend, você pode usar `npm start` com hot reload, sem rebuild de todo o container