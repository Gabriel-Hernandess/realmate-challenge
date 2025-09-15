# Realmate Challenge - Desafio Técnico

Este projeto foi desenvolvido como parte de um **desafio técnico**. Ele consiste em um sistema backend em **Django** com autenticação JWT via cookies e um frontend em **React** para gerenciamento de conversas recebidos de webhook, com funções assíncronas e uso de IA (Groq) para geração de relatórios agendados.

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
- Gerar relatórios por IA (Groq) a cada 24hrs de cada conversa com base em suas últimas 50 mensagens
- APIs de conversas:
  - Listar todas as conversas
  - Consultar conversa específica pelo `pk` (conforme desafio)
  - Consultar os relatórios de conversa especifica pelo `pk`
  - API de webhook (conforme desafio)
- Todas as rotas bases do desafio técnico são acessíveis sem autenticação
- Rotas extras exigem Token JWT via Cookies

### Frontend

- Página de login
- Dashboard com:
  - Menu lateral
  - Lista de conversas
  - Modal de mensagens estilo WhatsApp (balões, direção e data)
  - Último relatório da conversa gerado por IA
  - Tela de rotas (APIs)
  - Logout com confirmação

---
