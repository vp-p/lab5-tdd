"""Exercício 1 - Classificação de triângulos.

O programa recebe três valores inteiros (os lados) e informa se formam um
triângulo equilátero, isósceles ou escaleno. A condição de existência é que a
soma de quaisquer dois lados seja maior que o terceiro; lados menores ou iguais
a zero também não formam triângulo.
"""

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
        if not Triangulo._forma_triangulo(a, b, c):
            return TipoTriangulo.INVALIDO
        if a == b == c:
            return TipoTriangulo.EQUILATERO
        if a == b or a == c or b == c:
            return TipoTriangulo.ISOSCELES
        return TipoTriangulo.ESCALENO

    @staticmethod
    def _forma_triangulo(a: int, b: int, c: int) -> bool:
        lados_positivos = a > 0 and b > 0 and c > 0
        desigualdade_triangular = a + b > c and a + c > b and b + c > a
        return lados_positivos and desigualdade_triangular
