from ortools.sat.python import cp_model
import random

def gerar_killer_sudoku(num_cages=30, seed=42):
    model = cp_model.CpModel()

    ORDEM = 9
    RAIZ = 3
    # VARIÁVEIS: cell[i][j] representa a célula na linha i e coluna j
    cell = {}
    for i in range(ORDEM):
        for j in range(ORDEM):
            cell[(i,j)] = model.NewIntVar(1,9,f"cell_{i}_{j}")

    # restrição: linhas all-different
    for i in range(ORDEM):
        model.AddAllDifferent([cell[(i,j)] for j in range(ORDEM)])

    # restrição: colunas all-different
    for j in range(ORDEM):
        model.AddAllDifferent([cell[(i,j)] for i in range(ORDEM)])

    # restrição: blocos 3x3 all-different
    for bi in range(0, ORDEM, RAIZ):
        for bj in range(0, ORDEM, RAIZ):
            bloco = []
            for i in range(RAIZ):
                for j in range(RAIZ):
                    bloco.append(cell[(bi+i, bj+j)])
            model.AddAllDifferent(bloco)


    # config solver
    solver = cp_model.CpSolver()
    #heuristica dde busca
    solver.parameters.random_seed = 2134
    solver.parameters.search_branching = cp_model.PORTFOLIO_SEARCH
    solver.parameters.num_search_workers = 4
    solver.parameters.max_time_in_seconds = 5.0

    status = solver.Solve(model)
    if status != cp_model.OPTIMAL and status != cp_model.FEASIBLE:
        raise RuntimeError("Não consegui gerar uma solução de Sudoku clássico.")

    # agora temos uma grade completa válida
    solucao = [[solver.Value(cell[(i,j)]) for j in range(ORDEM)] for i in range(ORDEM)]

    # ------------------------------------------------
    # criar cages aleatórias a partir da solução
    # ------------------------------------------------
    todas_celulas = [(i,j) for i in range(ORDEM) for j in range(ORDEM)]
    random.shuffle(todas_celulas)

    cages = []
    usados = set()
    while todas_celulas:
        inicio = todas_celulas.pop()
        if inicio in usados:
            continue
        cage = [inicio]
        usados.add(inicio)

        # tamanho aleatório entre 1 e 4 células
        tamanho = random.randint(1,4)

        # tentar expandir cage com células vizinhas
        fronteira = [inicio]
        while len(cage) < tamanho and fronteira:
            i,j = fronteira.pop()
            vizinhos = [(i+1,j),(i-1,j),(i,j+1),(i,j-1)]
            random.shuffle(vizinhos)
            for v in vizinhos:
                if v in usados: continue
                if 0 <= v[0] < ORDEM and 0 <= v[1] < ORDEM:
                    cage.append(v)
                    usados.add(v)
                    fronteira.append(v)
                if len(cage) >= tamanho:
                    break

        soma = sum(solucao[i][j] for i,j in cage)
        # converter para formato (coluna, linha) 1-based
        cages.append(([(j+1,i+1) for i,j in cage], soma))

    return solucao, cages


sol, killer = gerar_killer_sudoku(num_cages=40, seed=2145)

print("=== Solução completa ===")
for linha in sol:
    print(linha)


print("\n=== Cages geradas ===")
for cage in killer:
    print(cage, ",")
