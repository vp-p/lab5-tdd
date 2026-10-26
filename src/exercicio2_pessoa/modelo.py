"""Modelo de domínio do Exercício 2, conforme o diagrama de classes.

    Person 1 ----- 1..* Email   ("possui")
"""

from dataclasses import dataclass, field


@dataclass
class Email:
    id: int
    name: str


@dataclass
class Person:
    id: int
    name: str
    age: int
    emails: list[Email] = field(default_factory=list)
