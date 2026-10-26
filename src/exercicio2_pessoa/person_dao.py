"""Exercício 2 - PersonDAO.

`is_valid_to_include` devolve a lista de erros de validação de uma `Person`
(lista vazia = pode ser incluída). Regras:

1. O nome tem ao menos 2 partes e é composto somente de letras;
2. A idade está no intervalo [1, 200];
3. A pessoa tem ao menos um objeto `Email` associado;
4. Cada e-mail tem o formato "_____@____._____", com ao menos um caractere
   em cada parte.
"""

import re

from exercicio2_pessoa.modelo import Email, Person

MSG_NOME_PARTES = "O nome deve ter ao menos 2 partes"
MSG_NOME_LETRAS = "O nome deve ser composto apenas de letras"
MSG_IDADE = "A idade deve estar entre 1 e 200"
MSG_EMAIL_OBRIGATORIO = "A pessoa deve ter ao menos um e-mail"

IDADE_MINIMA = 1
IDADE_MAXIMA = 200

# parte-local @ dominio . sufixo -> cada parte com 1+ caracteres
_FORMATO_EMAIL = re.compile(r"[^@\s]+@[^@\s.]+\.[^@\s.]+")


def msg_email_invalido(endereco) -> str:
    return f"E-mail inválido: {endereco}"


class PersonDAO:
    def __init__(self) -> None:
        self._pessoas: list[Person] = []

    @property
    def pessoas(self) -> list[Person]:
        return list(self._pessoas)

    def save(self, p: Person) -> None:
        """Inclui `p` (em memória). Levanta ValueError se não for válida."""
        erros = self.is_valid_to_include(p)
        if erros:
            raise ValueError("; ".join(erros))
        self._pessoas.append(p)

    def is_valid_to_include(self, p: Person) -> list[str]:
        """Retorna os erros que impedem a inclusão de `p` (vazia se válida)."""
        return [
            *self._validar_nome(p),
            *self._validar_idade(p),
            *self._validar_emails(p),
        ]

    # Alias com o nome exato usado no diagrama de classes (Java).
    isValidToInclude = is_valid_to_include

    @staticmethod
    def _validar_nome(p: Person) -> list[str]:
        erros = []
        partes = (p.name or "").split()
        if len(partes) < 2:
            erros.append(MSG_NOME_PARTES)
        if not all(parte.isalpha() for parte in partes):
            erros.append(MSG_NOME_LETRAS)
        return erros

    @staticmethod
    def _validar_idade(p: Person) -> list[str]:
        idade_valida = (
            isinstance(p.age, int) and IDADE_MINIMA <= p.age <= IDADE_MAXIMA
        )
        return [] if idade_valida else [MSG_IDADE]

    @staticmethod
    def _validar_emails(p: Person) -> list[str]:
        if not p.emails:
            return [MSG_EMAIL_OBRIGATORIO]
        return [
            msg_email_invalido(email.name)
            for email in p.emails
            if not PersonDAO._email_valido(email)
        ]

    @staticmethod
    def _email_valido(email: Email) -> bool:
        return isinstance(email.name, str) and bool(
            _FORMATO_EMAIL.fullmatch(email.name)
        )
