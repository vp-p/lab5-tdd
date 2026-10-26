"""Testes do Exercício 2: PersonDAO.is_valid_to_include (TDD)."""

from exercicio2_pessoa.modelo import Email, Person
from exercicio2_pessoa.person_dao import PersonDAO


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
