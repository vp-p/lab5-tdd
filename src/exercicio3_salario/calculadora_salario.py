"""Exercício 3 - Calculadora de salário líquido.

Cada cargo tem uma regra com duas faixas de desconto separadas por um limite:
salário base >= limite paga o desconto maior; abaixo dele, o desconto menor.

    Cargo          limite        desconto (>= limite)   desconto (< limite)
    DESENVOLVEDOR  3.000,00      20%                    10%
    DBA            2.000,00      25%                    15%
    TESTADOR       2.000,00      25%                    15%
    GERENTE        5.000,00      30%                    20%
"""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

from exercicio3_salario.funcionario import Cargo, Funcionario

CENTAVO = Decimal("0.01")


@dataclass(frozen=True)
class RegraDesconto:
    limite: Decimal
    desconto_a_partir_do_limite: Decimal
    desconto_abaixo_do_limite: Decimal

    def desconto_para(self, salario_base: Decimal) -> Decimal:
        if salario_base >= self.limite:
            return self.desconto_a_partir_do_limite
        return self.desconto_abaixo_do_limite


REGRAS_POR_CARGO: dict[Cargo, RegraDesconto] = {
    Cargo.DESENVOLVEDOR: RegraDesconto(
        Decimal("3000.00"), Decimal("0.20"), Decimal("0.10")
    ),
    Cargo.DBA: RegraDesconto(Decimal("2000.00"), Decimal("0.25"), Decimal("0.15")),
    Cargo.TESTADOR: RegraDesconto(
        Decimal("2000.00"), Decimal("0.25"), Decimal("0.15")
    ),
    Cargo.GERENTE: RegraDesconto(
        Decimal("5000.00"), Decimal("0.30"), Decimal("0.20")
    ),
}


class CalculadoraSalario:
    def calcular_salario_liquido(self, funcionario: Funcionario) -> Decimal:
        """Salário base menos o desconto do cargo, arredondado em centavos."""
        regra = REGRAS_POR_CARGO[funcionario.cargo]
        desconto = regra.desconto_para(funcionario.salario_base)
        liquido = funcionario.salario_base * (1 - desconto)
        return liquido.quantize(CENTAVO, rounding=ROUND_HALF_UP)
