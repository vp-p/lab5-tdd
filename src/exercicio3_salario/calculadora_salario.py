"""Calculadora de salário líquido (fase GREEN: DESENVOLVEDOR, DBA)."""

from decimal import ROUND_HALF_UP, Decimal

from exercicio3_salario.funcionario import Cargo, Funcionario


class CalculadoraSalario:
    def calcular_salario_liquido(self, funcionario: Funcionario) -> Decimal:
        if funcionario.cargo is Cargo.DESENVOLVEDOR:
            if funcionario.salario_base >= Decimal("3000.00"):
                desconto = Decimal("0.20")
            else:
                desconto = Decimal("0.10")
        elif funcionario.cargo is Cargo.DBA:
            if funcionario.salario_base >= Decimal("2000.00"):
                desconto = Decimal("0.25")
            else:
                desconto = Decimal("0.15")
        else:
            raise NotImplementedError
        liquido = funcionario.salario_base * (1 - desconto)
        return liquido.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
