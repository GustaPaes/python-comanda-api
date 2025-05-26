# GUSTAVO PAES DE LIZ

from fastapi import APIRouter
from domain.entities.Funcionario import Funcionario
import db
from infra.orm.FuncionarioModel import FuncionarioDB

# import da segurança
from typing import Annotated
from fastapi import Depends
from security import get_current_active_user, User
import bcrypt

# dependências de forma global
router = APIRouter( dependencies=[Depends(get_current_active_user)] )

@router.get("/funcionario/", tags=["Funcionário"])
async def get_funcionario():
    try:
        session = db.Session()

        # busca todos
        dados = session.query(FuncionarioDB).all()

        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.get("/funcionario/{id}", tags=["Funcionário"])
async def get_funcionario(id: int):
    try:
        session = db.Session()

        # busca um com filtro
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.id_funcionario == id).all()

        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.post("/funcionario/", tags=["Funcionário"])
async def post_funcionario(corpo: Funcionario):
    try:
        session = db.Session()
        
        # Gera o hash da senha
        senha_hash = bcrypt.hashpw(corpo.senha.encode('utf-8'), bcrypt.gensalt())
        
        dados = FuncionarioDB(
            None, 
            corpo.nome, 
            corpo.matricula,
            corpo.cpf, 
            corpo.telefone, 
            corpo.grupo, 
            senha_hash.decode('utf-8')  # Armazena o hash como string
        )

        session.add(dados)
        session.commit()

        return {"id": dados.id_funcionario}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.put("/funcionario/{id}", tags=["Funcionário"])
async def put_funcionario(id: int, corpo: Funcionario):
    try:
        session = db.Session()
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.id_funcionario == id).one()

        # Atualiza a senha somente se foi enviada nova senha
        if corpo.senha:
            senha_hash = bcrypt.hashpw(corpo.senha.encode('utf-8'), bcrypt.gensalt())
            dados.senha = senha_hash.decode('utf-8')

        # Mantém os outros campos
        dados.nome = corpo.nome
        dados.cpf = corpo.cpf
        dados.telefone = corpo.telefone
        dados.matricula = corpo.matricula
        dados.grupo = corpo.grupo
        
        session.add(dados)
        session.commit()

        return {"id": dados.id_funcionario}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.delete("/funcionario/{id}", tags=["Funcionário"])
async def delete_funcionario(id: int):
    try:
        session = db.Session()
        
        # busca os dados atuais pelo id
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.id_funcionario == id).one()

        session.delete(dados)
        session.commit()

        return {"id": dados.id_funcionario}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

# valida o cpf e senha informado pelo usuário
@router.post("/funcionario/login/", tags=["Funcionário - Login"])
async def login_funcionario(corpo: Funcionario):
    try:
        session = db.Session()

        # Busca somente pelo CPF
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.cpf == corpo.cpf).one()
        
        # Verifica a senha usando bcrypt
        if not bcrypt.checkpw(corpo.senha.encode('utf-8'), dados.senha.encode('utf-8')):
            raise ValueError("Credenciais inválidas")

        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 401  # 401 Unauthorized
    finally:
        session.close()

# verifica se o CPF informado já esta cadastrado, retornado os dados atuais caso já esteja
@router.get("/funcionario/cpf/{cpf}", tags=["Funcionário - Valida CPF"])
async def cpf_funcionario(cpf: str):
    try:
        session = db.Session()

        # busca um com filtro, retornando os dados cadastrados
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.cpf == cpf).all()
        
        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()