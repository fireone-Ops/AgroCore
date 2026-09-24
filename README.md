# AgroCore

Sistema web desenvolvido para auxiliar no **gerenciamento de propriedades rurais**, centralizando informações relacionadas a fazendas, culturas, estoque, maquinário e operações agrícolas.

O projeto utiliza uma arquitetura **full-stack**, com backend desenvolvido em **Python/Django**, banco de dados **PostgreSQL** e uma interface web separada no frontend.

---

## Tecnologias

### Backend

* Python
* Django
* Django REST Framework
* PostgreSQL

### Frontend

* JavaScript
* React
* Vite
* Tailwind CSS
* ESLint

---

## Funcionalidades

* Gerenciamento de usuários.
* Cadastro e gerenciamento de fazendas.
* Controle de culturas agrícolas.
* Gerenciamento de estoque.
* Controle de maquinário.
* Sistema de solicitações.
* Sistema de alertas.
* Registro de auditoria das operações.
* API para comunicação entre frontend e backend.
* Interface web para gerenciamento das informações.

---

## Estrutura do Projeto

```text
AgroCore/
├── backend/
│   ├── accounts/
│   ├── alertas/
│   ├── auditoria/
│   ├── config/
│   ├── culturas/
│   ├── estoque/
│   ├── fazendas/
│   ├── maquinario/
│   └── solicitacoes/
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── manage.py
├── .gitignore
└── README.md
```

---

## Requisitos

Para executar o projeto é necessário possuir:

* Python 3
* pip
* PostgreSQL
* Node.js
* npm

---

## Como executar

Clone o repositório:

```bash
git clone https://github.com/fireone-Ops/AgroCore.git
```

Entre na pasta:

```bash
cd AgroCore
```

### Backend

Crie um ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente virtual.

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

Instale as dependências do backend:

```bash
pip install -r requirements.txt
```

Configure a conexão com o banco de dados PostgreSQL através das variáveis de ambiente utilizadas pelo projeto.

Execute as migrações:

```bash
python manage.py migrate
```

Inicie o servidor:

```bash
python manage.py runserver
```

---

### Frontend

Em outro terminal, entre na pasta do frontend:

```bash
cd frontend
```

Instale as dependências:

```bash
npm install
```

Inicie o servidor de desenvolvimento:

```bash
npm run dev
```

---

## Funcionamento

O AgroCore centraliza diferentes áreas da administração de uma propriedade rural.

O frontend envia requisições para a API disponibilizada pelo backend Django, responsável pelo processamento das informações e comunicação com o banco de dados PostgreSQL.

Fluxo simplificado:

```text
Usuário
   │
   ▼
Frontend
React + Vite
   │
   ▼
API
Django REST Framework
   │
   ▼
Regras de Negócio
   │
   ▼
PostgreSQL
```

Os módulos do backend são separados de acordo com as responsabilidades do sistema:

```text
AgroCore
   │
   ├── Accounts
   │      └── Usuários e autenticação
   │
   ├── Fazendas
   │      └── Propriedades rurais
   │
   ├── Culturas
   │      └── Culturas agrícolas
   │
   ├── Estoque
   │      └── Controle de insumos e produtos
   │
   ├── Maquinário
   │      └── Máquinas e equipamentos
   │
   ├── Solicitações
   │      └── Gerenciamento de solicitações
   │
   ├── Alertas
   │      └── Notificações do sistema
   │
   └── Auditoria
          └── Registro de operações
```

---

## Arquitetura

O projeto utiliza uma arquitetura dividida entre **frontend e backend**, com o PostgreSQL responsável pela persistência dos dados.

```text
┌─────────────────┐
│    Frontend     │
│  React + Vite   │
└────────┬────────┘
         │
         │ HTTP / API
         ▼
┌─────────────────┐
│     Django      │
│    REST API     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Regras de       │
│ Negócio         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   PostgreSQL    │
└─────────────────┘
```

---

## Melhorias Futuras

* Implementação de dashboards com indicadores da propriedade.
* Relatórios de produção agrícola.
* Controle financeiro.
* Histórico de produtividade das culturas.
* Gerenciamento de custos por propriedade.
* Integração com APIs meteorológicas.
* Alertas relacionados a estoque e operações.
* Testes automatizados.
* Containerização com Docker.
* Criação de modelo de LLM, com integração com o landset para previsão de plantar e colher.
* Usar visão computacional para controle de pragas e doenças
---

## Aprendizados

Este projeto permite aprofundar conhecimentos em:

* Desenvolvimento backend com Python.
* Desenvolvimento web com Django.
* Criação de APIs REST.
* Desenvolvimento frontend com React.
* Integração entre frontend e backend.
* PostgreSQL e bancos de dados relacionais.
* Modelagem de banco de dados.
* Autenticação e gerenciamento de usuários.
* Organização de aplicações Django em módulos.
* Desenvolvimento de sistemas full-stack.
* Estruturação de projetos de software.
