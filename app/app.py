import panel as pn
import pandas as pd

pn.extension('tabulator', notifications=True)

titulo_disc = pn.pane.Markdown("# 📚 Gerenciar Disciplinas")
input_nome_disc = pn.widgets.TextInput(name='Nome da Disciplina', placeholder='Ex: Cálculo I')
input_carga_disc = pn.widgets.IntInput(name='Carga Horária', value=64, step=16)
btn_salvar_disc = pn.widgets.Button(name='Salvar Disciplina', button_type='primary')
btn_deletar_disc = pn.widgets.Button(name='Deletar Selecionada', button_type='danger')
tabela_disc = pn.widgets.Tabulator(pd.DataFrame({'Status': ['Carregando...']}), layout='fit_data_stretch')

titulo_user = pn.pane.Markdown("# 👥 Gerenciar Usuários")
input_nome_user = pn.widgets.TextInput(name='Nome do Usuário', placeholder='Ex: João Victor')
input_cpf_user = pn.widgets.TextInput(name='CPF', placeholder='Ex: 123.456.789-00')
input_email_user = pn.widgets.TextInput(name='E-mail', placeholder='Ex: joao@alu.ufc.br')
btn_salvar_user = pn.widgets.Button(name='Salvar Usuário', button_type='success')
btn_deletar_user = pn.widgets.Button(name='Deletar Selecionado', button_type='danger')
tabela_user = pn.widgets.Tabulator(pd.DataFrame({'Status': ['Carregando...']}), layout='fit_data_stretch')

def carregar_dados_do_banco():
    try:
        from database import engine
        from esquema import Disciplina, Usuario
        from sqlalchemy.orm import sessionmaker
        
        SessionLocal = sessionmaker(bind=engine)
        db = SessionLocal()
        
        df_disc = pd.read_sql(db.query(Disciplina).statement, db.bind)
        if not df_disc.empty: 
            tabela_disc.value = df_disc
            
        df_user = pd.read_sql(db.query(Usuario).statement, db.bind)
        if not df_user.empty: 
            tabela_user.value = df_user
            
        db.close()
    except Exception as e:
        erro_df = pd.DataFrame({'Erro': ['Falha de Conexão'], 'Detalhe': [str(e)[:80]]})
        tabela_disc.value = erro_df
        tabela_user.value = erro_df

carregar_dados_do_banco()

def salvar_disc(event):
    try:
        from database import engine
        from esquema import Disciplina
        from sqlalchemy.orm import sessionmaker
        db = sessionmaker(bind=engine)()
        
        nova = Disciplina(nome=input_nome_disc.value, carga_horaria=input_carga_disc.value)
        db.add(nova)
        db.commit()
        db.close()
        
        carregar_dados_do_banco()
        pn.state.notifications.success('Disciplina salva com sucesso!')
    except Exception as e:
        pn.state.notifications.error('Erro ao salvar disciplina. Verifique o terminal.')

def deletar_disc(event):
    try:
        if len(tabela_disc.selection) > 0:
            from database import engine
            from esquema import Disciplina
            from sqlalchemy.orm import sessionmaker
            db = sessionmaker(bind=engine)()
            
            id_sel = int(tabela_disc.value.iloc[tabela_disc.selection[0]]['id_disciplina'])
            db.query(Disciplina).filter(Disciplina.id_disciplina == id_sel).delete()
            db.commit()
            db.close()
            
            carregar_dados_do_banco()
            pn.state.notifications.info('Disciplina removida do sistema.')
    except Exception as e:
        pn.state.notifications.error('Erro ao deletar disciplina.')

def salvar_user(event):
    try:
        from database import engine
        from esquema import Usuario
        from sqlalchemy.orm import sessionmaker
        db = sessionmaker(bind=engine)()
        
        novo = Usuario(nome=input_nome_user.value, cpf=input_cpf_user.value, email=input_email_user.value)
        db.add(novo)
        db.commit()
        db.close()
        
        carregar_dados_do_banco()
        pn.state.notifications.success('Usuário registrado com sucesso!')
    except Exception as e:
        print(f"\n[LOG DE ERRO DO BANCO]:\n{e}\n")
        pn.state.notifications.error('Erro ao registrar usuário. Verifique as restrições (ex: CPF duplicado).')

def deletar_user(event):
    try:
        if len(tabela_user.selection) > 0:
            from database import engine
            from esquema import Usuario
            from sqlalchemy.orm import sessionmaker
            db = sessionmaker(bind=engine)()
            
            id_sel = int(tabela_user.value.iloc[tabela_user.selection[0]]['id_usuario'])
            db.query(Usuario).filter(Usuario.id_usuario == id_sel).delete()
            db.commit()
            db.close()
            
            carregar_dados_do_banco()
            pn.state.notifications.info('Usuário removido do sistema.')
    except Exception as e:
        pn.state.notifications.error('Erro ao deletar usuário.')

btn_salvar_disc.on_click(salvar_disc)
btn_deletar_disc.on_click(deletar_disc)
btn_salvar_user.on_click(salvar_user)
btn_deletar_user.on_click(deletar_user)

tela_disciplinas = pn.Column(
    titulo_disc,
    pn.Row(input_nome_disc, input_carga_disc),
    pn.Row(btn_salvar_disc, btn_deletar_disc),
    tabela_disc
)

tela_usuarios = pn.Column(
    titulo_user,
    pn.Row(input_nome_user, input_cpf_user, input_email_user),
    pn.Row(btn_salvar_user, btn_deletar_user),
    tabela_user
)

sistema_completo = pn.Tabs(
    ("📚 Disciplinas", tela_disciplinas),
    ("👥 Usuários", tela_usuarios)
)

sistema_completo.servable()