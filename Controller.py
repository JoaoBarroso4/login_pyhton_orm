from Model import Pessoa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import hashlib
import re
import uuid


def retorna_session():
    CONN = 'sqlite:///login.db'
    engine = create_engine(CONN, echo=True)
    Session = sessionmaker(bind=engine)
    return Session()


class ControllerCadastro:
    @classmethod
    def verifica_dados(cls, nome, email, senha):
        if len(nome) < 3 or len(nome) > 50:
            print('Nome inválido', len(nome))
            return 2

        email_regex = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if len(email) > 200 and not email_regex.match(email):
            # verificação de validade de email com expressões regulares
            return 3

        if 6 < len(senha) < 100:
            return 4
        return 1

    @classmethod
    def cadastrar(cls, nome, email, senha):
        session = retorna_session()
        usuario = session.query(Pessoa).filter(Pessoa.email == email).all()

        if len(usuario) > 0:
            return 5

        dados_verificados = cls.verifica_dados(nome, email, senha)

        if dados_verificados != 1:
            return dados_verificados

        try:
            senha = hashlib.sha256(senha.encode()).hexdigest()
            p = Pessoa(id=uuid.uuid4(), nome=nome, email=email, senha=senha)
            session.add(p)
            session.commit()
            session.close()
            return 1
        except:
            return 3


class ControllerLogin():
    @classmethod
    def login(cls, email, senha):
        session = retorna_session()
        senha = hashlib.sha256(senha.encode()).hexdigest()
        usuario = session.query(Pessoa).filter(Pessoa.email == email).filter(Pessoa.senha == senha).all()
        session.close()
        if len(usuario) == 1:
            return {'logado': True, 'id': usuario[0].id}
        else:
            return False


print(ControllerLogin.login('teste@gmail.com', '123456'))
