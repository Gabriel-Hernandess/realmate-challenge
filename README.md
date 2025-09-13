# Realmate Challenge - Desafio Técnico

Este projeto foi desenvolvido como parte de um **desafio técnico**. Ele consiste em um sistema backend em **Django** com autenticação JWT via cookies e um frontend em **React** para gerenciamento de conversas recebidos de webhook.

---

## Tecnologias

- **Backend:** Django, Django REST Framework, SimpleJWT, Celery
- **Frontend:** React
- **Banco de Dados:** PostgreSQL
- **Cache / Broker:** Redis
- **Containerização:** Docker e Docker Compose
- **Gerenciamento de dependências:** Poetry

---

## Funcionalidades

### Backend

- Autenticação via JWT (login, refresh token, logout)
- Registro automático de superuser ao iniciar o container
- APIs de conversas:
  - Listar todas as conversas
  - Consultar conversa específica pelo `pk` (desafio)
- API de webhook (conforme desafio)
- Todas as rotas do desafio técnico são acessíveis sem autenticação
- Rota de logout exige autenticação

### Frontend

- Página de login
- Dashboard com:
  - Menu lateral
  - Lista de conversas
  - Modal de mensagens estilo WhatsApp (balões, direção e data)
  - Tela de rotas (APIs)
  - Logout com confirmação

---
