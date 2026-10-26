"""Casos de teste do Exercício 1 (Triângulo).

Cada situação pedida no enunciado está em uma seção própria. Quando o enunciado
pede "um CT para cada permutação", os testes são parametrizados e cada
permutação aparece como um caso de teste distinto no relatório do pytest.
"""

from itertools import permutations

import pytest

from exercicio1_triangulo.triangulo import TipoTriangulo, Triangulo


def classificar(a, b, c):
    return Triangulo.classificar(a, b, c)


# --- Triângulos válidos -----------------------------------------------------


def test_escaleno_valido():
    assert classificar(3, 4, 5) == TipoTriangulo.ESCALENO


def test_equilatero_valido():
    assert classificar(3, 3, 3) == TipoTriangulo.EQUILATERO


def test_isosceles_valido():
    assert classificar(5, 5, 8) == TipoTriangulo.ISOSCELES


# Isósceles válido: permutações distintas dos mesmos valores (2, 2, 3).
@pytest.mark.parametrize("a, b, c", [(2, 2, 3), (2, 3, 2), (3, 2, 2)])
def test_isosceles_valido_permutacoes(a, b, c):
    assert classificar(a, b, c) == TipoTriangulo.ISOSCELES


# --- Valores inválidos: zero e negativo --------------------------------------


@pytest.mark.parametrize("a, b, c", [(0, 4, 5), (4, 0, 5), (4, 5, 0)])
def test_um_valor_zero(a, b, c):
    assert classificar(a, b, c) == TipoTriangulo.INVALIDO


@pytest.mark.parametrize("a, b, c", [(-3, 4, 5), (3, -4, 5), (3, 4, -5)])
def test_um_valor_negativo(a, b, c):
    assert classificar(a, b, c) == TipoTriangulo.INVALIDO


def test_tres_valores_zero():
    assert classificar(0, 0, 0) == TipoTriangulo.INVALIDO


# --- Desigualdade triangular ---------------------------------------------------
# A soma de dois lados tem que ser MAIOR que o terceiro lado.


# Soma de 2 lados IGUAL ao terceiro (1 + 2 = 3): um CT para cada permutação.
@pytest.mark.parametrize("a, b, c", sorted(set(permutations((1, 2, 3)))))
def test_soma_de_dois_lados_igual_ao_terceiro(a, b, c):
    assert classificar(a, b, c) == TipoTriangulo.INVALIDO


# Soma de 2 lados MENOR que o terceiro (1 + 2 < 4): um CT para cada permutação.
@pytest.mark.parametrize("a, b, c", sorted(set(permutations((1, 2, 4)))))
def test_soma_de_dois_lados_menor_que_o_terceiro(a, b, c):
    assert classificar(a, b, c) == TipoTriangulo.INVALIDO


# Casos de fronteira extras: valores iguais não podem mascarar a violação.
@pytest.mark.parametrize("a, b, c", [(2, 2, 4), (2, 4, 2), (4, 2, 2)])
def test_isosceles_degenerado_nao_e_triangulo(a, b, c):
    assert classificar(a, b, c) == TipoTriangulo.INVALIDO
