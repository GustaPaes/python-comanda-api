# GUSTAVO PAES DE LIZ

from fastapi import APIRouter
from domain.entities.Produto import Produto
import db
from infra.orm.ProdutoModel import ProdutoDB
import base64

# import da segurança
from typing import Annotated
from fastapi import Depends
from security import get_current_active_user, User

# dependências de forma global
router = APIRouter( dependencies=[Depends(get_current_active_user)] )

def converter_base64_para_bytes(base64_string):
    base64_bytes = base64_string.split(",")[1]  # Remove o prefixo 'data:image/png;base64,'
    return base64.b64decode(base64_bytes)

@router.get("/produto/", tags=["Produto"])
async def get_produto():
    try:
        session = db.Session()

        # busca todos
        dados = session.query(ProdutoDB).all()

        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.get("/produto/{id}", tags=["Produto"])
async def get_produto(id: int):
    try:
        session = db.Session()

        # busca um com filtro
        dados = session.query(ProdutoDB).filter(ProdutoDB.id_produto == id).all()

        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.post("/produto/", tags=["Produto"])
async def post_produto(corpo: Produto):
    try:
        session = db.Session()

        if corpo.foto is not None:
            foto_bytes = converter_base64_para_bytes(corpo.foto)
        else:
            foto_bytes = None

        # cria um novo objeto com os dados da requisição
        dados = ProdutoDB(None, corpo.nome, corpo.descricao, foto_bytes, corpo.valor_unitario)

        session.add(dados)
        # session.flush()
        session.commit()

        return {"id": dados.id_produto}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.put("/produto/{id}", tags=["Produto"])
async def put_produto(id: int, corpo: Produto):
    try:
        session = db.Session()

        # busca os dados atuais pelo id
        dados = session.query(ProdutoDB).filter(ProdutoDB.id_produto == id).one()

        # atualiza os dados com base no corpo da requisição
        dados.nome = corpo.nome
        dados.descricao = corpo.descricao
        if corpo.foto is not None:
            dados.foto = converter_base64_para_bytes(corpo.foto)
        dados.valor_unitario = corpo.valor_unitario
        
        session.add(dados)
        session.commit()

        return {"id": dados.id_produto}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.delete("/produto/{id}", tags=["Produto"])
async def delete_produto(id: int):
    try:
        session = db.Session()
        
        # busca os dados atuais pelo id
        dados = session.query(ProdutoDB).filter(ProdutoDB.id_produto == id).one()

        session.delete(dados)
        session.commit()

        return {"id": dados.id_produto}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()