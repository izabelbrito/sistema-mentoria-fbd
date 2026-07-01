# 📚 Sistema de Mentoria - CRUD

Projeto prático desenvolvido para a disciplina de Fundamentos de Bancos de Dados. O sistema permite o gerenciamento de disciplinas de mentoria e o cadastro de usuários através de uma interface web conectada a um banco de dados relacional.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Interface Web:** Panel / Bokeh
* **Banco de Dados:** PostgreSQL
* **ORM:** SQLAlchemy
* **Manipulação de Dados:** Pandas

## ⚙️ Como executar o projeto

1. Clone este repositório.
2. Crie um ambiente virtual e ative-o.
3. Instale as dependências: `pip install panel pandas sqlalchemy psycopg2-binary`
4. Configure as credenciais do seu banco PostgreSQL no arquivo `app/database.py`.
5. Execute os scripts SQL (`banco/create.sql` e `banco/insert.sql`) no seu gerenciador de banco (ex: pgAdmin).
6. Inicie o servidor web rodando o comando na pasta `app`:
  
   ```bash
   python -m panel serve app.py --show