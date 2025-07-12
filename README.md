
# 🩺 Voluntários da Saúde — Backend Flask com Painel de Administração

Este é o backend completo da landing page de uma ONG chamada **Voluntários da Saúde**. O projeto foi desenvolvido **do zero** com foco em segurança, boas práticas RESTful, validações robustas, autenticação JWT e integração com frontend HTML estático.

---

## 📦 Tecnologias utilizadas

- Python 3.11
- Flask
- PostgreSQL
- JWT (JSON Web Token)
- Limiter (controle de requisições)
- `uuid`, `os`, `dotenv`, `werkzeug`, etc.
- Integração com **Discord** para envio de logs
- Estrutura de arquivos baseada em Blueprints e modularização

---

## 🧠 Objetivo do projeto

Desenvolver um **painel administrativo** e sistema de APIs para gerenciamento completo da landing page da ONG, permitindo que o administrador possa:

- Gerenciar **eventos**
- Gerenciar **atualizações**
- Receber **formulários do site** (seja voluntário, doações, fale conosco)
- Autenticar via **JWT**
- Visualizar logs em tempo real via **Discord**

---

## 📁 Estrutura de pastas

```bash
.
├── static/                   # Arquivos estáticos (CSS, JS, imagens e uploads)
│   ├── img/
│   ├── scripts/
│   ├── styles/
│   ├── uploads/             # Imagens dos eventos
│   └── uploads_att/         # Imagens das atualizações
│
├── templates/               # Páginas HTML da landing page
│   ├── index.html
│   ├── login.html
│   ├── doacao.html
│   ├── fale_conosco.html
│   ├── seja_voluntario.html
│   ├── sobreNos.html
│   └── transparencia.html
│
├── funcoes/                 # Validações customizadas
│   ├── validar_email.py
│   ├── validar_mensagem.py
│   └── validar_telefone.py
│
├── routes/
│   ├── api/                 # Endpoints RESTful organizados com Blueprints
│   │   ├── fale_conosco.py
│   │   ├── seja_voluntario.py
│   │   ├── doacao.py
│   │   ├── adicionar_evento.py
│   │   ├── update.py
│   │   ├── listar_eventos.py
│   │   ├── deletar_eventos.py
│   │   ├── adicionar_att.py
│   │   ├── update_att.py
│   │   ├── listar_att.py
│   │   ├── deletar_att.py
│   │   └── login.py
│   ├── db/
│   │   └── conexao.py       # Conexão com o PostgreSQL
│   └── utils/
│       ├── jwt_decoder.py   # Decodificação e verificação de JWT
│       └── logger.py        # Logger com integração ao Discord
│
├── .env                     # Variáveis de ambiente (SECRET, DB, Discord)
├── app.py                   # Inicialização da aplicação Flask
└── requirements.txt         # Dependências do projeto
```

---

## 🔐 Autenticação

- O painel administrativo (`/admin/eventos`) é protegido via **JWT**.
- O token pode ser enviado via cookie ou header `Authorization: Bearer <token>`.
- Caso o token esteja expirado ou inválido, o usuário é redirecionado para o `index.html`.

---

## 🔄 Endpoints implementados

### 🔐 Login (JWT)
- `POST /api/login`  
  - Recebe e valida usuário e senha, retornando o token JWT.

### 📍 Área Administrativa (protegida por token)

#### 📅 Eventos
- `GET /api/eventos`
- `POST /api/eventos`
- `PUT /api/eventos/<id>`
- `DELETE /api/eventos/<id>`

#### 🔁 Atualizações
- `GET /api/atualizacao`
- `POST /api/atualizacao`
- `PUT /api/atualizacao/<id>`
- `DELETE /api/atualizacao/<id>`

### 🌐 Formulários Públicos

#### 🤝 Seja voluntário
- `POST /api/seja_voluntario`

#### 💬 Fale conosco
- `POST /api/fale_conosco`

#### 💸 Doação
- `POST /api/doacao`

---

## 📊 Log em tempo real no Discord

Logs como erros, acessos não autorizados e sucesso nas operações são enviados para um canal Discord.

---

## ✅ Funcionalidades implementadas

- [x] Backend RESTful completo
- [x] CRUDs com imagem
- [x] Autenticação JWT segura
- [x] Logger com Discord
- [x] Limitação de requisições
- [x] HTML renderizado diretamente do backend
- [x] Validação robusta de entradas
- [x] Modularização com Blueprints

---

## 🚀 Como rodar localmente

```bash
git clone https://github.com/seuusuario/voluntarios-backend.git
cd voluntarios-backend
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
# Crie um .env com as variáveis necessárias
python app.py
```

---

## 👤 Desenvolvedor

**Ryan M.**  
Estudante de Análise e Desenvolvimento de Sistemas - FATEC Franca  
Desenvolvedor Backend Python (Flask, PostgreSQL, APIs RESTful)  
Contato: [LinkedIn](https://www.linkedin.com/in/ryan-moscardini-b7b6372ba) | [GitHub](https://github.com/ryanmosc)

---

## 🧪 Próximas melhorias

- [ ] Deploy em nuvem (Render, Railway, etc.)
- [ ] Migrar todo o sistema para Java + Springboot
- [ ] Dashboard de controle interno e analise de dados
