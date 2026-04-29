# 💰 FinanceControl

> Sistema de controle de finanças pessoais com tema Cyberpunk Dark - Full Stack com Flask!

![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-371C1C?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

---

## 📋 Sobre

O **FinanceControl** é uma aplicação web full-stack para controle de finanças pessoais com:
- **Backend**: Flask com autenticação segura e API REST
- **Frontend**: Dashboard intuitivo com tema Cyberpunk Dark
- **Banco de dados**: SQLite3 com relacionamentos ORM
- **Funcionalidades**: Login, cadastro, criar/deletar transações, relatórios

---

## ✨ Funcionalidades

- 🔐 **Autenticação segura** - Login e cadastro com senhas criptografadas (PBKDF2)
- 📊 **Dashboard financeiro** - Resumo de saldo, receitas, despesas e economia
- ➕ **CRUD de transações** - Criar, visualizar e deletar transações
- 💾 **Banco de dados persistente** - SQLite com relacionamentos
- 🏷️ **Categorias** - Alimentação, Transporte, Saúde, Lazer, Salário, Outros
- ✅ **Validação dupla** - Front-end e back-end
- 📱 **Responsivo** - Desktop, tablet e mobile
- 🎨 **Design moderno** - Cyberpunk Dark com efeitos glow
- 🔌 **API REST** - Endpoints JSON

---

## 🚀 Iniciar

### Opção 1: Usar o script (Mais fácil)
```bash
./start.sh
```

### Opção 2: Manual
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

**Acesse**: `http://localhost:5000`

---

## 🎯 Primeiros passos

1. Clique em **"Cadastre-se gratuitamente"**
2. Preencha os dados (CPF e telefone têm máscara automática)
3. **Faça login** com suas credenciais
4. No dashboard, clique em **"+ Nova Transação"** para adicionar receitas/despesas
5. Veja o **resumo financeiro atualizar em tempo real**
6. Clique no **🗑️** para deletar uma transação

---

## 📁 Estrutura

```
finance-control/
├── app.py                      # Backend Flask (modelos, rotas, API)
├── requirements.txt            # Dependências Python
├── start.sh                    # Script para iniciar
├── .gitignore                  # Ignore venv e .db
│
├── static/
│   └── style.css               # Tema Cyberpunk Dark
│
├── templates/
│   ├── login.html              # Login
│   ├── cadastro.html           # Cadastro
│   ├── dashboard.html          # Dashboard
│   ├── erro_404.html           # Erro 404
│   └── erro_500.html           # Erro 500
│
├── instance/
│   └── finance_control.db      # BD SQLite (criado automaticamente)
│
└── venv/                       # Ambiente Python (criado automaticamente)
```

---

## 🔌 API Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Redireciona para login ou dashboard |
| POST | `/login` | Fazer login (JSON) |
| POST | `/cadastro` | Criar conta (JSON) |
| GET | `/logout` | Sair |
| GET | `/dashboard` | Dashboard financeiro |
| GET | `/api/transacoes` | Listar transações |
| POST | `/api/transacoes` | Criar transação |
| DELETE | `/api/transacoes/<id>` | Deletar transação |
| GET | `/api/relatorio` | Relatório do mês |

---

## 🎨 Paleta de Cores

| Cor | Código | Uso |
|-----|--------|-----|
| Ciano | `#00ffe7` | Primária |
| Roxo | `#b57bee` | Secundária |
| Verde | `#39d353` | Receitas |
| Vermelho | `#ff6b6b` | Despesas |
| Amarelo | `#e3b341` | Alimentação |
| Fundo | `#0d1117` | Canvas |

---

## 🔒 Segurança

- ✅ Senhas criptografadas com PBKDF2
- ✅ Validação de entrada (front-end + back-end)
- ✅ Email e CPF únicos
- ✅ Sessões seguras com Flask-Login
- ✅ Proteção contra SQL injection (SQLAlchemy ORM)

---

## 🐛 Troubleshooting

### Porta 5000 em uso
```python
# No final do app.py:
app.run(debug=True, host='0.0.0.0', port=8000)
```

### Banco de dados corrompido
```bash
rm instance/finance_control.db
python app.py
```

### Erro de módulos
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🧪 Testar com cURL

### Login
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"usuario@email.com","senha":"senha123"}'
```

### Criar transação
```bash
curl -X POST http://localhost:5000/api/transacoes \
  -H "Content-Type: application/json" \
  -d '{"descricao":"Supermercado","valor":150.50,"tipo":"despesa","categoria":"alimentacao"}'
```

### Obter relatório
```bash
curl http://localhost:5000/api/relatorio
```

---

## 📚 Tecnologias

- **Backend**: Flask 2.3.3, SQLAlchemy, Flask-Login
- **Frontend**: HTML5, CSS3, JavaScript vanilla
- **Database**: SQLite3
- **Segurança**: Werkzeug (PBKDF2)

---

## 💡 Ideias para expansão

- [ ] Gráficos com Chart.js
- [ ] Filtros avançados
- [ ] Editar transações
- [ ] Exportar para CSV/PDF
- [ ] Temas customizáveis
- [ ] Notificações por email
- [ ] Integração com bancos reais

---

## 👩‍💻 Autora

Desenvolvido com ❤️ por **Maristela Oliveira**  
[github.com/MARISTELAOLIVEIRA](https://github.com/MARISTELAOLIVEIRA)

**Status**: ✅ Pronto para desenvolvimento
**Versão**: 1.0
**Última atualização**: 29 de Abril de 2026
