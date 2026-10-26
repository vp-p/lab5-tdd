"""Testes do Exercício 2: PersonDAO.is_valid_to_include (TDD)."""

import pytest

from exercicio2_pessoa.modelo import Email, Person
from exercicio2_pessoa.person_dao import (
    MSG_NOME_LETRAS,
    MSG_NOME_PARTES,
    PersonDAO,
)


def pessoa_valida(**alteracoes) -> Person:
    dados = {
        "id": 1,
        "name": "Maria Silva",
        "age": 30,
        "emails": [Email(1, "maria@exemplo.com")],
    }
    dados.update(alteracoes)
    return Person(**dados)


def test_pessoa_valida_nao_retorna_erros():
    assert PersonDAO().is_valid_to_include(pessoa_valida()) == []


# --- Regra 1: nome com ao menos 2 partes, composto de letras -----------------


@pytest.mark.parametrize(
    "nome", ["Maria Silva", "Maria da Silva", "José Ângelo", "Ana  Maria"]
)
def test_nome_com_duas_ou_mais_partes_de_letras_e_valido(nome):
    assert PersonDAO().is_valid_to_include(pessoa_valida(name=nome)) == []


@pytest.mark.parametrize("nome", ["Maria", "", "   ", None])
def test_nome_com_menos_de_duas_partes_e_invalido(nome):
    erros = PersonDAO().is_valid_to_include(pessoa_valida(name=nome))
    assert erros == [MSG_NOME_PARTES]


@pytest.mark.parametrize("nome", ["Maria S1lva", "Maria Silva3", "Maria Silva!", "M@ria Silva"])
def test_nome_com_caractere_que_nao_e_letra_e_invalido(nome):
    erros = PersonDAO().is_valid_to_include(pessoa_valida(name=nome))
    assert erros == [MSG_NOME_LETRAS]


def test_nome_de_uma_parte_e_com_numero_acumula_os_dois_erros():
    erros = PersonDAO().is_valid_to_include(pessoa_valida(name="Mar1a"))
    assert erros == [MSG_NOME_PARTES, MSG_NOME_LETRAS]
