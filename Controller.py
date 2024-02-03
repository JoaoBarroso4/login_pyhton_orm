from Model import Pessoa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import re
import hashlib
import uuid


def retorna_session():
    CONN = 'sqlite:///login.db'
    engine = create_engine(CONN, echo=True)
    Session = sessionmaker(bind=engine)
    return Session()


class ControllerCadastro:
    SUCCESS = 1
    ERROR_INVALID_NAME = 2
    ERROR_INVALID_EMAIL = 3
    ERROR_INVALID_PASSWORD = 4
    ERROR_USER_EXISTS = 5


    @staticmethod
    def verifica_dados(nome, email, senha):
        if len(nome) < 3 or len(nome) > 50:
            print('Nome inválido', len(nome))
            return ControllerCadastro.ERROR_INVALID_NAME

        email_regex = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if len(email) > 200 and not email_regex.match(email):
            return ControllerCadastro.ERROR_INVALID_EMAIL

        if 6 < len(senha) < 100:
            return ControllerCadastro.ERROR_INVALID_PASSWORD
        return ControllerCadastro.SUCCESS

    @staticmethod
    def cadastrar(nome, email, senha):
        session = retorna_session()
        usuario = session.query(Pessoa).filter(Pessoa.email == email).all()

        if len(usuario) > 0:
            return ControllerCadastro.ERROR_USER_EXISTS

        dados_verificados = ControllerCadastro.verifica_dados(nome, email, senha)

        if dados_verificados != ControllerCadastro.SUCCESS:
            return dados_verificados

        try:
            senha = hashlib.sha256(senha.encode()).hexdigest()
            p = Pessoa(id=uuid.uuid4(), nome=nome, email=email, senha=senha)
            session.add(p)
            session.commit()
            session.close()
            return ControllerCadastro.SUCCESS
        except Exception as e:
            print(f"Erro interno: {str(e)}")
            return


class ControllerLogin:
    @staticmethod
    def login(email, senha):
        session = retorna_session()
        senha = hashlib.sha256(senha.encode()).hexdigest()
        usuario = session.query(Pessoa).filter(Pessoa.email == email).filter(Pessoa.senha == senha).all()
        session.close()
        if len(usuario) == 1:
            return {'logado': True, 'id': usuario[0].id}
        else:
            return False
