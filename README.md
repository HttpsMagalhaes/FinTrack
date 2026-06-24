# FinTrack

Sistema web para rastreamento, visualização e comparação de ativos do mercado financeiro brasileiro em tempo real.

## Sobre o Projeto

O **FinTrack** foi desenvolvido com o objetivo de facilitar o acompanhamento e a análise de ativos financeiros por meio de uma interface simples e intuitiva. A plataforma permite consultar informações atualizadas, visualizar gráficos de desempenho, comparar ativos e personalizar a experiência do usuário através do sistema de favoritos.

O projeto foi desenvolvido como parte das atividades acadêmicas do curso de Ciência da Computação, aplicando conceitos de Engenharia de Software, Desenvolvimento Web, Banco de Dados e Integração de APIs.

---

## 🎯 Funcionalidades

* 📊 Visualização de ativos financeiros em tempo real
* 📈 Exibição de gráficos históricos e de desempenho
* 🔍 Comparação entre diferentes ativos
* ⭐ Gerenciamento de ativos favoritos
* 👤 Cadastro e autenticação de usuários
* 🔐 Armazenamento seguro de credenciais
* 🌐 Integração com API de dados financeiros

---

## 🛠️ Tecnologias Utilizadas

### Backend

* Python
* Django

### Frontend

* HTML5
* CSS3

### Banco de Dados

* PostgreSQL

### Integrações

* yFinance API

### Ferramentas

* Git
* GitHub
* Notion


## Como Executar o Projeto

### Pré-requisitos

* Python 3.11+
* PostgreSQL
* Git

### Clonar o Repositório

```bash
git clone https://github.com/HttpsMagalhaes/FinTrack.git
cd fintrack
```

### Criar Ambiente Virtual

```bash
python -m venv venv
```

### Ativar Ambiente Virtual

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Instalar Dependências

```bash
pip install -r requirements.txt
```

### Configurar Banco de Dados

Configure as credenciais do PostgreSQL no arquivo de configuração do Django.

### Executar Migrações

```bash
python manage.py migrate
```

### Iniciar Servidor

```bash
python manage.py runserver
```
