# 💰 Controle Financeiro Web

Aplicação web para gerenciamento de receitas e despesas, desenvolvida em **Python + Flask + SQLite**.

O projeto foi estruturado como uma aplicação real, com separação por módulos, persistência em banco de dados, validação, interface web responsiva e testes automatizados.

## 🚀 Funcionalidades

- Cadastro de receitas e despesas
- Edição de lançamentos
- Exclusão de lançamentos
- Filtro por tipo de lançamento
- Dashboard com:
  - Total de receitas
  - Total de despesas
  - Saldo atual
- Persistência dos dados em SQLite
- Validação de formulários
- Interface responsiva
- Testes automatizados com Pytest

## 🛠️ Tecnologias

- Python 3
- Flask
- SQLite
- HTML5
- CSS3
- Pytest
- Git / GitHub

## 📁 Estrutura

```text
controle_financeiro_web/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── repository.py
│   ├── routes.py
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   └── templates/
│       ├── base.html
│       ├── index.html
│       └── form.html
├── tests/
│   ├── conftest.py
│   └── test_app.py
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

## ▶️ Como executar

### 1. Criar ambiente virtual

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Executar

```bash
python run.py
```

Abra no navegador:

```text
http://127.0.0.1:5000
```

## 🧪 Testes

```bash
pytest
```

## 📌 Próximas melhorias

- Autenticação de usuários
- Categorias personalizadas
- Gráficos por mês e categoria
- Exportação para CSV/PDF
- API REST
- PostgreSQL
- Deploy em nuvem

## 👨‍💻 Autor

**João Oliveira**  
Estudante de Engenharia de Software — 4º semestre  
GitHub: [@Oliveira7-Dev](https://github.com/Oliveira7-Dev)
