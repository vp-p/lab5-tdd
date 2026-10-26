"""Exercício 1 - Classificação de triângulos (fase GREEN)."""

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
        if a <= 0 or b <= 0 or c <= 0:
            return TipoTriangulo.INVALIDO
        if a + b <= c or a + c <= b or b + c <= a:
            return TipoTriangulo.INVALIDO
        if a == b == c:
            return TipoTriangulo.EQUILATERO
        if a == b or a == c or b == c:
            return TipoTriangulo.ISOSCELES
        return TipoTriangulo.ESCALENO
