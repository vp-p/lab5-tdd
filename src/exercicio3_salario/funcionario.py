"""Modelo de domínio do Exercício 3."""

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class Cargo(Enum):
    DESENVOLVEDOR = "DESENVOLVEDOR"
    DBA = "DBA"
    TESTADOR = "TESTADOR"
    GERENTE = "GERENTE"


@dataclass
class Funcionario:
    nome: str
    email: str
    salario_base: Decimal
    cargo: Cargo
