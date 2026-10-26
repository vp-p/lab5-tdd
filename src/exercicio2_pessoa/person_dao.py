"""PersonDAO."""

from exercicio2_pessoa.modelo import Person

MSG_NOME_PARTES = "O nome deve ter ao menos 2 partes"
MSG_NOME_LETRAS = "O nome deve ser composto apenas de letras"


class PersonDAO:
    def is_valid_to_include(self, p: Person) -> list[str]:
        return []
