# 🧩 Killer Sudoku Solvers

Este projeto implementa um solver de Killer Sudoku utilizando o **CP-SAT Solver do OR-Tools**.

> Para fins comparativos, também foi implementado o solver MIP de Killer Sudoku desenvolvido por [Aapeli Vuorinen](https://www.aapelivuorinen.com/blog/2023/01/18/killer-sudoku-mip).

Abaixo está a documentação do CP-SAT:

# CPSAT OR-Tools

## Início

A função `killer_sudoku_solver` é definida para resolver o Killer Sudoku. Ela recebe como entrada `data`, uma lista de gaiolas contendo suas respectivas células e soma alvo. O modelo de propagação de restrições é criado usando o CP-SAT Solver.

```python
def killer_sudoku_solver(data):
    model = cp_model.CpModel()
```

## Definição de Constantes

```python
ORDEM = 9
RAIZ = 3
```

Define-se a ordem do grid e a raiz, baseando-se no Sudoku padrão 9x9.

## Variáveis de decisão

```python
cell = {}
for i in range(ORDEM):
    for j in range(ORDEM):
        cell[(i,j)] = model.NewIntVar(1,9,f"cell_{i}_{j}")
```

Cria-se um dicionário cell com variáveis inteiras para cada célula do Sudoku, todas com domínio de 1 a 9. Começa na indexação 0, e vai até 8 (no caso da ordem 9).

## Restrições

### linhas AllDifferent

```python
for i in range(ORDEM):
    model.AddAllDifferent([cell[(i,j)] for j in range(ORDEM)])
```

### colunas AllDifferent

```python
for i in range(ORDEM):
    model.AddAllDifferent([cell[(i,j)] for j in range(ORDEM)])
```

### blocos 3x3 AllDifferent

```python
for bi in range(0, ORDEM, RAIZ):
    for bj in range(0, ORDEM, RAIZ):
        bloco = []
        for i in range(RAIZ):
            for j in range(RAIZ):
                bloco.append(cell[(bi+i, bj+j)])
        model.AddAllDifferent(bloco)
```

### gaiolas 3x3 AllDifferent

```python
for cage in data:
    celulas, soma = cage
    vars_cage = []
    for (coluna, linha) in celulas:
        v = (linha-1, coluna-1)
        vars_cage.append(cell[v])
    model.AddAllDifferent(vars_cage)
    model.Add(sum(vars_cage) == soma)
```

## Configuração do solver

```python
solver = cp_model.CpSolver()
solver.parameters.log_search_progress = True
solver.parameters.num_search_workers = 4
```

Instancia-se o solver e configura-se:

- Logs de progresso de busca ativados.
- Paralelismo com 4 threads.
