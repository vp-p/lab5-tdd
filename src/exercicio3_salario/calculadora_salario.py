"""Calculadora de salário líquido (esqueleto - fase RED)."""

from decimal import Decimal

from exercicio3_salario.funcionario import Funcionario


class CalculadoraSalario:
    def calcular_salario_liquido(self, funcionario: Funcionario) -> Decimal:
        raise NotImplementedError
