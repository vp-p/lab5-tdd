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
