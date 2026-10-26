"""Testes do Exercício 2: PersonDAO.is_valid_to_include (TDD)."""

import pytest

from exercicio2_pessoa.modelo import Email, Person
from exercicio2_pessoa.person_dao import (
    MSG_EMAIL_OBRIGATORIO,
    MSG_IDADE,
    MSG_NOME_LETRAS,
    MSG_NOME_PARTES,
    PersonDAO,
    msg_email_invalido,
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


# --- Regra 4: e-mail no formato "_____@____._____" ----------------------------
# Cada uma das três partes (antes do @, entre @ e ponto, depois do ponto)
# precisa ter ao menos um caractere.


@pytest.mark.parametrize(
    "endereco", ["a@b.c", "maria@exemplo.com", "m.silva@empresa.org", "x_y-1@d.io"]
)
def test_email_no_formato_correto_e_valido(endereco):
    pessoa = pessoa_valida(emails=[Email(1, endereco)])
    assert PersonDAO().is_valid_to_include(pessoa) == []


@pytest.mark.parametrize(
    "endereco",
    [
        "",  # vazio
        "semarroba.com",  # sem @
        "a@b",  # sem ponto depois do @
        "@b.c",  # parte antes do @ vazia
        "a@.c",  # parte entre @ e ponto vazia
        "a@b.",  # parte depois do ponto vazia
        "a@@b.c",  # dois @
        "a b@c.d",  # espaço
        "a@b.c.d",  # mais de um ponto depois do @ (fora do formato)
        None,  # sem endereço
    ],
)
def test_email_fora_do_formato_e_invalido(endereco):
    pessoa = pessoa_valida(emails=[Email(1, endereco)])
    erros = PersonDAO().is_valid_to_include(pessoa)
    assert erros == [msg_email_invalido(endereco)]


def test_um_erro_por_email_invalido_mantendo_os_validos():
    emails = [Email(1, "ok@exemplo.com"), Email(2, "ruim"), Email(3, "pior@")]
    erros = PersonDAO().is_valid_to_include(pessoa_valida(emails=emails))
    assert erros == [msg_email_invalido("ruim"), msg_email_invalido("pior@")]


def test_todas_as_regras_violadas_acumulam_os_erros():
    pessoa = Person(1, "Maria", 0, [Email(1, "invalido")])
    erros = PersonDAO().is_valid_to_include(pessoa)
    assert erros == [MSG_NOME_PARTES, MSG_IDADE, msg_email_invalido("invalido")]


def test_alias_com_o_nome_do_diagrama_de_classes():
    dao = PersonDAO()
    pessoa = pessoa_valida(age=0)
    assert dao.isValidToInclude(pessoa) == dao.is_valid_to_include(pessoa) == [MSG_IDADE]


# --- save(p): void (presente no diagrama) -------------------------------------
# Persistência em memória: só inclui pessoas válidas.


def test_save_inclui_pessoa_valida():
    dao = PersonDAO()
    pessoa = pessoa_valida()
    dao.save(pessoa)
    assert dao.pessoas == [pessoa]


def test_save_rejeita_pessoa_invalida_informando_os_erros():
    dao = PersonDAO()
    with pytest.raises(ValueError) as excecao:
        dao.save(pessoa_valida(age=0))
    assert MSG_IDADE in str(excecao.value)
    assert dao.pessoas == []
