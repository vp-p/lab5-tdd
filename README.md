# Exercícios de TDD com Python e pytest

Implementação dos três exercícios de **JUnit e TDD** da disciplina, em
**Python 3 com pytest** (cobertura com **pytest-cov**). Todo o código foi
desenvolvido com o ciclo **Red → Green → Refactor**, e o histórico do git
registra cada etapa (veja [Histórico TDD](#histórico-tdd)).

| Exercício | Tema | Testes | Cobertura (linhas / ramos) |
|-----------|------|:------:|:--------------------------:|
| 1 | Classificação de triângulos | 28 | 100% / 100% |
| 2 | `PersonDAO.isValidToInclude()` | 46 | 100% / 100% |
| 3 | Calculadora de salário líquido | 26 | 100% / 100% |
| **Total** | | **100** | **100%** |

## Pré-requisitos

- Python 3.10 ou superior
- `pip` (acompanha o Python)

## Build (preparar o ambiente)

Não há etapa de compilação: o "build" é criar o ambiente virtual e instalar as
dependências de teste (`pytest` e `pytest-cov`).

```bash
# 1. clonar o repositório e entrar na pasta
git clone <URL-DO-REPOSITORIO>
cd tdd-exercicios

# 2. criar e ativar o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate          # Windows (PowerShell): .venv\Scripts\Activate.ps1

# 3. instalar as dependências
pip install -r requirements.txt
```

## Executando os testes

A configuração do pytest está no `pyproject.toml` (já inclui `src/` no
`PYTHONPATH`), então basta rodar a partir da raiz do projeto:

```bash
# todos os exercícios
pytest

# um exercício por vez, com o nome de cada caso de teste
pytest tests/exercicio1_triangulo -v
pytest tests/exercicio2_pessoa -v
pytest tests/exercicio3_salario -v
```

## Cobertura de código por teste

Os comandos abaixo geram a cobertura **de linhas e de ramos** (`--cov-branch`)
de cada exercício, listando as linhas não cobertas (`term-missing`):

```bash
pytest tests/exercicio1_triangulo --cov=exercicio1_triangulo --cov-branch --cov-report=term-missing
pytest tests/exercicio2_pessoa    --cov=exercicio2_pessoa    --cov-branch --cov-report=term-missing
pytest tests/exercicio3_salario   --cov=exercicio3_salario   --cov-branch --cov-report=term-missing

# visão geral dos três exercícios
pytest --cov --cov-branch --cov-report=term-missing

# (opcional) relatório HTML navegável em htmlcov/index.html
pytest --cov --cov-branch --cov-report=html
```

A saída completa de cada execução (com o nome e o resultado de cada teste)
está salva em [`docs/cobertura/`](docs/cobertura/).

## Estrutura do projeto

```
.
├── pyproject.toml            # configuração do pytest e do coverage
├── requirements.txt          # pytest, pytest-cov
├── src/
│   ├── exercicio1_triangulo/ # triangulo.py
│   ├── exercicio2_pessoa/    # modelo.py (Person, Email), person_dao.py
│   └── exercicio3_salario/   # funcionario.py, calculadora_salario.py
├── tests/
│   ├── exercicio1_triangulo/test_triangulo.py
│   ├── exercicio2_pessoa/test_person_dao.py
│   └── exercicio3_salario/test_calculadora_salario.py
└── docs/cobertura/           # saídas do pytest-cov de cada exercício
```

---

## Exercício 1 - Triângulo

**Código:** [`src/exercicio1_triangulo/triangulo.py`](src/exercicio1_triangulo/triangulo.py) ·
**Testes:** [`tests/exercicio1_triangulo/test_triangulo.py`](tests/exercicio1_triangulo/test_triangulo.py)

`Triangulo.classificar(a, b, c)` recebe três inteiros e devolve um
`TipoTriangulo`: `EQUILATERO`, `ISOSCELES`, `ESCALENO` ou `INVALIDO`. Os lados
formam um triângulo quando todos são positivos e a soma de quaisquer dois é
**maior** que o terceiro.

### Casos de teste x requisitos do enunciado

| Situação pedida | Teste | Casos (CTs) |
|-----------------|-------|:-----------:|
| Triângulo escaleno válido | `test_escaleno_valido` | 1 - (3, 4, 5) |
| Triângulo isósceles válido | `test_isosceles_valido` | 1 - (5, 5, 8) |
| Triângulo equilátero válido | `test_equilatero_valido` | 1 - (3, 3, 3) |
| Isósceles válido: 3+ CTs com permutações dos mesmos valores | `test_isosceles_valido_permutacoes` | 3 - (2,2,3), (2,3,2), (3,2,2) |
| Um valor zero | `test_um_valor_zero` | 3 - zero em cada posição |
| Um valor negativo | `test_um_valor_negativo` | 3 - negativo em cada posição |
| Soma de 2 lados **igual** ao terceiro, um CT por permutação | `test_soma_de_dois_lados_igual_ao_terceiro` | 6 - permutações de (1, 2, 3) |
| Soma de 2 lados **menor** que o terceiro, um CT por permutação | `test_soma_de_dois_lados_menor_que_o_terceiro` | 6 - permutações de (1, 2, 4) |
| Os três valores iguais a zero | `test_tres_valores_zero` | 1 - (0, 0, 0) |
| *(extra)* isósceles "degenerado" não é triângulo | `test_isosceles_degenerado_nao_e_triangulo` | 3 - permutações de (2, 2, 4) |

Total: **28 casos de teste**.

### Evidência de cobertura

```text
Name                                    Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------------------------------------
src/exercicio1_triangulo/__init__.py        0      0      0      0   100%
src/exercicio1_triangulo/triangulo.py      21      0      6      0   100%
-----------------------------------------------------------------------------------
TOTAL                                      21      0      6      0   100%

28 passed in 0.13s
```

---

## Exercício 2 - `PersonDAO.isValidToInclude()`

**Código:** [`modelo.py`](src/exercicio2_pessoa/modelo.py) e
[`person_dao.py`](src/exercicio2_pessoa/person_dao.py) ·
**Testes:** [`tests/exercicio2_pessoa/test_person_dao.py`](tests/exercicio2_pessoa/test_person_dao.py)

O modelo segue o diagrama de classes: `Person(id, name, age)` está associada a
`1..*` `Email(id, name)` (relação "possui"), e `PersonDAO` possui
`save(p): void` e `isValidToInclude(p): List<String>`.

`PersonDAO.is_valid_to_include(p)` devolve a **lista de mensagens de erro**
(lista vazia = a pessoa pode ser incluída). Regras validadas, todas acumulando
erros (não para no primeiro):

| # | Regra | Mensagem |
|---|-------|----------|
| 1 | O nome tem ao menos 2 partes | `O nome deve ter ao menos 2 partes` |
| 1 | O nome é composto somente de letras (aceita acentos) | `O nome deve ser composto apenas de letras` |
| 2 | A idade está no intervalo [1, 200] | `A idade deve estar entre 1 e 200` |
| 3 | Há ao menos um `Email` associado | `A pessoa deve ter ao menos um e-mail` |
| 4 | Cada e-mail tem o formato `_____@____._____` (cada parte com 1+ caractere) | `E-mail inválido: <endereço>` |

Decisões de implementação:

- O método se chama `is_valid_to_include` (snake_case, convenção do Python) e
  também está disponível como `isValidToInclude`, o nome usado no diagrama.
- Cada e-mail inválido gera **um** erro próprio, e os válidos da mesma pessoa
  não são afetados.
- O formato do e-mail é o do enunciado, estrito: parte local, `@`, domínio, um
  único `.` e sufixo. Por isso `a@b.c.d` é considerado inválido. A parte local
  aceita pontos (`m.silva@empresa.org`).
- `save(p)` também está no diagrama, então foi implementado de forma mínima e
  também com TDD: persiste em memória e levanta `ValueError` (com os erros) se a
  pessoa não for válida.

### Evidência de cobertura

```text
Name                                  Stmts   Miss Branch BrPart  Cover   Missing
---------------------------------------------------------------------------------
src/exercicio2_pessoa/__init__.py         0      0      0      0   100%
src/exercicio2_pessoa/modelo.py          11      0      0      0   100%
src/exercicio2_pessoa/person_dao.py      46      0      8      0   100%
---------------------------------------------------------------------------------
TOTAL                                    57      0      8      0   100%

46 passed in 0.16s
```

---

## Exercício 3 - Calculadora de salário

**Código:** [`funcionario.py`](src/exercicio3_salario/funcionario.py) e
[`calculadora_salario.py`](src/exercicio3_salario/calculadora_salario.py) ·
**Testes:** [`tests/exercicio3_salario/test_calculadora_salario.py`](tests/exercicio3_salario/test_calculadora_salario.py)

`Funcionario(nome, email, salario_base, cargo)` e
`CalculadoraSalario.calcular_salario_liquido(funcionario)`. O salário base
**maior ou igual** ao limite paga o desconto maior:

| Cargo | Limite | Desconto (>= limite) | Desconto (< limite) |
|-------|-------:|:--------------------:|:-------------------:|
| DESENVOLVEDOR | 3.000,00 | 20% | 10% |
| DBA | 2.000,00 | 25% | 15% |
| TESTADOR | 2.000,00 | 25% | 15% |
| GERENTE | 5.000,00 | 30% | 20% |

Decisões de implementação:

- Valores monetários usam `decimal.Decimal` (sem erros de ponto flutuante) e o
  resultado é arredondado em centavos com `ROUND_HALF_UP`.
- Para cada cargo são testados valores **abaixo, exatamente no limite e acima**
  dele (por exemplo, 2.999,99 / 3.000,00 / 3.000,01 para DESENVOLVEDOR).
- No refactor final, o `if/elif` por cargo virou uma tabela de regras
  (`REGRAS_POR_CARGO`), sem alterar o comportamento nem os testes.

### Evidência de cobertura

```text
Name                                            Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------------------------------------------
src/exercicio3_salario/__init__.py                  0      0      0      0   100%
src/exercicio3_salario/calculadora_salario.py      20      0      2      0   100%
src/exercicio3_salario/funcionario.py              14      0      0      0   100%
-------------------------------------------------------------------------------------------
TOTAL                                              34      0      2      0   100%

26 passed in 0.13s
```

---

## Cobertura geral

```text
Name                                            Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------------------------------------------
src/exercicio1_triangulo/__init__.py                0      0      0      0   100%
src/exercicio1_triangulo/triangulo.py              21      0      6      0   100%
src/exercicio2_pessoa/__init__.py                   0      0      0      0   100%
src/exercicio2_pessoa/modelo.py                    11      0      0      0   100%
src/exercicio2_pessoa/person_dao.py                46      0      8      0   100%
src/exercicio3_salario/__init__.py                  0      0      0      0   100%
src/exercicio3_salario/calculadora_salario.py      20      0      2      0   100%
src/exercicio3_salario/funcionario.py              14      0      0      0   100%
-------------------------------------------------------------------------------------------
TOTAL                                             112      0     16      0   100%
```

## Histórico TDD

Cada exercício foi feito em ciclos: `test(...)` **RED** (teste escrito e
falhando), `feat(...)` **GREEN** (implementação mínima que passa) e
`refactor(...)` (melhoria com todos os testes verdes). Ordem dos commits:

```text
chore: estrutura inicial do projeto (pytest + pytest-cov)
test(ex1): RED - esqueleto do Triangulo e casos de teste
feat(ex1): GREEN - implementa classificacao de triangulos
refactor(ex1): extrai _forma_triangulo e documenta as regras
test(ex2): RED - modelo Person/Email e teste de pessoa valida
feat(ex2): GREEN - pessoa valida retorna lista vazia
test(ex2): RED - regra do nome (2+ partes e somente letras)
feat(ex2): GREEN - valida nome (2+ partes, somente letras)
test(ex2): RED - regra da idade [1, 200]
feat(ex2): GREEN - valida idade no intervalo [1, 200]
test(ex2): RED - pessoa deve ter ao menos um e-mail
feat(ex2): GREEN - exige ao menos um e-mail associado
test(ex2): RED - formato do e-mail (_____@____._____)
feat(ex2): GREEN - valida formato do e-mail
refactor(ex2): separa uma validacao por regra e adiciona alias isValidToInclude
test(ex2): RED - save(p) so inclui pessoas validas
feat(ex2): GREEN - save(p) valida antes de incluir
test(ex3): RED - desconto do DESENVOLVEDOR (esqueleto + testes)
feat(ex3): GREEN - desconto do DESENVOLVEDOR
test(ex3): RED - desconto do DBA
feat(ex3): GREEN - desconto do DBA
test(ex3): RED - desconto do TESTADOR
feat(ex3): GREEN - desconto do TESTADOR
test(ex3): RED - desconto do GERENTE
feat(ex3): GREEN - desconto do GERENTE
refactor(ex3): tabela de regras por cargo no lugar do if/elif
```
