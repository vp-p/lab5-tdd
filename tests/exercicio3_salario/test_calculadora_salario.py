"""Testes do Exercício 3: calculadora de salário líquido por cargo (TDD).

Para cada cargo há duas faixas de desconto, separadas por um limite. O limite
pertence à faixa de desconto MAIOR ("maior ou igual"), então cada cargo é
testado abaixo do limite, exatamente no limite e acima dele.
"""

from decimal import Decimal

import pytest

from exercicio3_salario.calculadora_salario import CalculadoraSalario
from exercicio3_salario.funcionario import Cargo, Funcionario


def liquido(cargo: Cargo, salario_base: str) -> Decimal:
    funcionario = Funcionario(
        nome="Fulano de Tal",
        email="fulano@empresa.com",
        salario_base=Decimal(salario_base),
        cargo=cargo,
    )
    return CalculadoraSalario().calcular_salario_liquido(funcionario)


# --- DESENVOLVEDOR: 20% se salário >= 3.000,00; senão 10% ----------------------


@pytest.mark.parametrize(
    "salario_base, esperado",
    [
        ("1000.00", "900.00"),  # abaixo do limite -> 10%
        ("2999.99", "2699.99"),  # logo abaixo do limite -> 10%
        ("3000.00", "2400.00"),  # exatamente no limite -> 20%
        ("3000.01", "2400.01"),  # logo acima do limite -> 20%
        ("5000.00", "4000.00"),  # acima do limite -> 20%
    ],
)
def test_desenvolvedor(salario_base, esperado):
    assert liquido(Cargo.DESENVOLVEDOR, salario_base) == Decimal(esperado)


# --- DBA: 25% se salário >= 2.000,00; senão 15% --------------------------------


@pytest.mark.parametrize(
    "salario_base, esperado",
    [
        ("1000.00", "850.00"),  # abaixo do limite -> 15%
        ("1999.99", "1699.99"),  # logo abaixo do limite -> 15%
        ("2000.00", "1500.00"),  # exatamente no limite -> 25%
        ("2000.01", "1500.01"),  # logo acima do limite -> 25%
        ("4000.00", "3000.00"),  # acima do limite -> 25%
    ],
)
def test_dba(salario_base, esperado):
    assert liquido(Cargo.DBA, salario_base) == Decimal(esperado)


# --- TESTADOR: 25% se salário >= 2.000,00; senão 15% ---------------------------


@pytest.mark.parametrize(
    "salario_base, esperado",
    [
        ("1000.00", "850.00"),  # abaixo do limite -> 15%
        ("1999.99", "1699.99"),  # logo abaixo do limite -> 15%
        ("2000.00", "1500.00"),  # exatamente no limite -> 25%
        ("2000.01", "1500.01"),  # logo acima do limite -> 25%
        ("4000.00", "3000.00"),  # acima do limite -> 25%
    ],
)
def test_testador(salario_base, esperado):
    assert liquido(Cargo.TESTADOR, salario_base) == Decimal(esperado)


# --- GERENTE: 30% se salário >= 5.000,00; senão 20% ----------------------------


@pytest.mark.parametrize(
    "salario_base, esperado",
    [
        ("1000.00", "800.00"),  # abaixo do limite -> 20%
        ("4999.99", "3999.99"),  # logo abaixo do limite -> 20%
        ("5000.00", "3500.00"),  # exatamente no limite -> 30%
        ("5000.01", "3500.01"),  # logo acima do limite -> 30%
        ("10000.00", "7000.00"),  # acima do limite -> 30%
    ],
)
def test_gerente(salario_base, esperado):
    assert liquido(Cargo.GERENTE, salario_base) == Decimal(esperado)
