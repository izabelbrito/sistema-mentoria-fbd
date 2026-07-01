import os
import pandas as pd
import sqlalchemy as sa
from dotenv import load_dotenv
import panel as pn
from pathlib import Path

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}?client_encoding=utf8"
engine = sa.create_engine(db_url)

pn.extension('tabulator', notifications=True)

def get_disciplinas():
    try:
        return pd.read_sql_query("SELECT id_disciplina, nome, carga_horaria FROM Disciplina", engine)
    except Exception:
        return pd.DataFrame(columns=['id_disciplina', 'nome', 'carga_horaria'])

def get_usuarios():
    try:
        return pd.read_sql_query("SELECT id_usuario, nome, cpf, email FROM Usuario", engine)
    except Exception:
        return pd.DataFrame(columns=['id_usuario', 'nome', 'cpf', 'email'])

tabela_disciplinas = pn.widgets.Tabulator(get_disciplinas(), selectable=True)
tabela_usuarios = pn.widgets.Tabulator(get_usuarios(), selectable=True)

nome_disc_input = pn.widgets.TextInput(name="Nome da Disciplina")
carga_disc_input = pn.widgets.IntInput(name="Carga Horária", value=64, step=1)

btn_salvar_disc = pn.widgets.Button(name="Salvar Disciplina", button_type="primary")
btn_del_disc = pn.widgets.Button(name="Deletar Selecionada", button_type="danger")

def inserir_disc(event):
    if not nome_disc_input.value: 
        pn.state.notifications.warning("Preencha o nome da disciplina.")
        return
    try:
        with engine.begin() as conn:
            conn.execute(sa.text("INSERT INTO Disciplina (nome, carga_horaria) VALUES (:n, :c)"),
                         {"n": nome_disc_input.value, "c": carga_disc_input.value})
        nome_disc_input.value = ''
        tabela_disciplinas.value = get_disciplinas()
        pn.state.notifications.success("Disciplina salva com sucesso!")
    except Exception as e: 
        pn.state.notifications.error("Erro ao salvar disciplina.")
        print(e)

def deletar_disc(event):
    selecao = tabela_disciplinas.selection
    if not selecao: 
        pn.state.notifications.warning("Selecione uma disciplina para deletar.")
        return
    try:
        ids_del = tabela_disciplinas.value.iloc[selecao]['id_disciplina'].tolist()
        with engine.begin() as conn:
            for id_val in ids_del:
                conn.execute(sa.text("DELETE FROM Disciplina WHERE id_disciplina = :id"), {"id": id_val})
        tabela_disciplinas.selection = []
        tabela_disciplinas.value = get_disciplinas()
        pn.state.notifications.success("Disciplina deletada com sucesso!")
    except Exception as e: 
        pn.state.notifications.error("Erro ao deletar disciplina.")
        print(e)

btn_salvar_disc.on_click(inserir_disc)
btn_del_disc.on_click(deletar_disc)

aba_disciplinas = pn.Column(
    pn.pane.Markdown("## 📚 Gerenciar Disciplinas"),
    pn.Row(nome_disc_input, carga_disc_input),
    pn.Row(btn_salvar_disc, btn_del_disc),
    tabela_disciplinas
)

nome_usu_input = pn.widgets.TextInput(name="Nome do Usuário", placeholder="Ex: João Victor")
cpf_usu_input = pn.widgets.TextInput(name="CPF", placeholder="Ex: 123.456.789-00")
email_usu_input = pn.widgets.TextInput(name="E-mail", placeholder="Ex: joao@alu.ufc.br")

btn_salvar_usu = pn.widgets.Button(name="Salvar Usuário", button_type="success")
btn_del_usu = pn.widgets.Button(name="Deletar Selecionada", button_type="danger")

def inserir_usu(event):
    if not nome_usu_input.value or not cpf_usu_input.value: 
        pn.state.notifications.warning("Preencha nome e CPF.")
        return
    try:
        with engine.begin() as conn:
            conn.execute(sa.text("INSERT INTO Usuario (nome, cpf, email) VALUES (:n, :c, :e)"),
                         {"n": nome_usu_input.value, "c": cpf_usu_input.value, "e": email_usu_input.value})
        nome_usu_input.value = ''
        cpf_usu_input.value = ''
        email_usu_input.value = ''
        tabela_usuarios.value = get_usuarios()
        pn.state.notifications.success("Usuário salvo com sucesso!")
    except Exception as e: 
        pn.state.notifications.error("Erro ao salvar usuário.")
        print(e)

def deletar_usu(event):
    selecao = tabela_usuarios.selection
    if not selecao: 
        pn.state.notifications.warning("Selecione um usuário para deletar.")
        return
    try:
        ids_del = tabela_usuarios.value.iloc[selecao]['id_usuario'].tolist()
        with engine.begin() as conn:
            for id_val in ids_del:
                conn.execute(sa.text("DELETE FROM Usuario WHERE id_usuario = :id"), {"id": id_val})
        tabela_usuarios.selection = []
        tabela_usuarios.value = get_usuarios()
        pn.state.notifications.success("Usuário deletado com sucesso!")
    except Exception as e: 
        pn.state.notifications.error("Erro ao deletar usuário.")
        print(e)

btn_salvar_usu.on_click(inserir_usu)
btn_del_usu.on_click(deletar_usu)

aba_usuarios = pn.Column(
    pn.pane.Markdown("## 👥 Gerenciar Usuários"),
    pn.Row(nome_usu_input, cpf_usu_input, email_usu_input),
    pn.Row(btn_salvar_usu, btn_del_usu),
    tabela_usuarios
)

tabs = pn.Tabs(
    ('📚 Disciplinas', aba_disciplinas),
    ('👥 Usuários', aba_usuarios),
    dynamic=True
)

tabs.servable()