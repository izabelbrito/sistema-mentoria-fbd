import os
import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine
from dotenv import load_dotenv
import panel as pn

load_dotenv()
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

cnx = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
engine = create_engine(cnx)

pn.extension('tabulator')

nome_input = pn.widgets.TextInput(name="Nome", placeholder="Digite o nome")
cpf_input = pn.widgets.TextInput(name="CPF", placeholder="Digite o CPF")
email_input = pn.widgets.TextInput(name="E-mail", placeholder="Digite o e-mail")

button_consultar = pn.widgets.Button(name='Consultar', button_type='primary')
button_inserir = pn.widgets.Button(name='Inserir', button_type='success')
button_atualizar = pn.widgets.Button(name='Atualizar', button_type='warning')
button_excluir = pn.widgets.Button(name='Excluir', button_type='danger')

def query_all():
    query = "select * from usuario"
    df = pd.read_sql_query(query, engine)
    return pn.widgets.Tabulator(df)

def on_inserir(event):
    with engine.connect() as conn:
        conn.execute(sa.text("INSERT INTO usuario (nome, cpf, email) VALUES (:n, :c, :e)"), 
                     {"n": nome_input.value, "c": cpf_input.value, "e": email_input.value})
        conn.commit()
    return query_all()

def on_atualizar(event):
    with engine.connect() as conn:
        conn.execute(sa.text("UPDATE usuario SET nome = :n, email = :e WHERE cpf = :c"), 
                     {"n": nome_input.value, "e": email_input.value, "c": cpf_input.value})
        conn.commit()
    return query_all()

button_inserir.on_click(on_inserir)
button_atualizar.on_click(on_atualizar)

layout = pn.Column(
    '# Sistema de Mentoria - Gerenciamento',
    nome_input, cpf_input, email_input,
    pn.Row(button_consultar, button_inserir, button_atualizar, button_excluir),
    pn.bind(query_all, button_consultar)
)

layout.servable()