"""Testes do Exercício 2: PersonDAO.is_valid_to_include (TDD)."""

import pytest

from exercicio2_pessoa.modelo import Email, Person
from exercicio2_pessoa.person_dao import (
    MSG_EMAIL_OBRIGATORIO,
    MSG_IDADE,
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


# --- Regra 2: idade no intervalo [1, 200] -------------------------------------


@pytest.mark.parametrize("idade", [1, 2, 30, 199, 200])
def test_idade_dentro_do_intervalo_e_valida(idade):
    assert PersonDAO().is_valid_to_include(pessoa_valida(age=idade)) == []


@pytest.mark.parametrize("idade", [0, -1, 201, 1000, None])
def test_idade_fora_do_intervalo_e_invalida(idade):
    erros = PersonDAO().is_valid_to_include(pessoa_valida(age=idade))
    assert erros == [MSG_IDADE]


# --- Regra 3: ao menos um Email associado -------------------------------------


@pytest.mark.parametrize("emails", [[], None])
def test_pessoa_sem_email_e_invalida(emails):
    erros = PersonDAO().is_valid_to_include(pessoa_valida(emails=emails))
    assert erros == [MSG_EMAIL_OBRIGATORIO]


def test_pessoa_com_varios_emails_validos_e_valida():
    emails = [Email(1, "maria@exemplo.com"), Email(2, "m.silva@empresa.org")]
    assert PersonDAO().is_valid_to_include(pessoa_valida(emails=emails)) == []
