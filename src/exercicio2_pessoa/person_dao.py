"""PersonDAO."""

from exercicio2_pessoa.modelo import Person

MSG_NOME_PARTES = "O nome deve ter ao menos 2 partes"
MSG_NOME_LETRAS = "O nome deve ser composto apenas de letras"
MSG_IDADE = "A idade deve estar entre 1 e 200"
MSG_EMAIL_OBRIGATORIO = "A pessoa deve ter ao menos um e-mail"


def msg_email_invalido(endereco) -> str:
    return f"E-mail inválido: {endereco}"


class PersonDAO:
    def is_valid_to_include(self, p: Person) -> list[str]:
        erros: list[str] = []
        partes = (p.name or "").split()
        if len(partes) < 2:
            erros.append(MSG_NOME_PARTES)
        if not all(parte.isalpha() for parte in partes):
            erros.append(MSG_NOME_LETRAS)
        if not isinstance(p.age, int) or not 1 <= p.age <= 200:
            erros.append(MSG_IDADE)
        if not p.emails:
            erros.append(MSG_EMAIL_OBRIGATORIO)
        return erros
