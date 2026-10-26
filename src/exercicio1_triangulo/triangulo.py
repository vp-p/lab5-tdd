"""Exercício 1 - Classificação de triângulos (esqueleto - fase RED)."""

from enum import Enum


class TipoTriangulo(Enum):
    EQUILATERO = "equilátero"
    ISOSCELES = "isósceles"
    ESCALENO = "escaleno"
    INVALIDO = "inválido"


class Triangulo:
    """Recebe três lados inteiros e informa o tipo do triângulo."""

    @staticmethod
    def classificar(a: int, b: int, c: int) -> TipoTriangulo:
        raise NotImplementedError
