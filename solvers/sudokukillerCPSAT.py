from ortools.sat.python import cp_model
from INSTANCES.instances import easy_data_1, medium_data_1, expert_data_1

generated = [
    ([(7, 8), (8, 8), (8, 7), (8, 6)], 18),
([(8, 9), (9, 9), (9, 8)], 12),
([(2, 5), (3, 5), (4, 5)], 12),
([(5, 8), (5, 7), (4, 7)], 16),
([(5, 4), (6, 4), (7, 4)], 22),
([(9, 7), (9, 6)], 11),
([(4, 4), (4, 3)], 14),
([(7, 9), (6, 9), (5, 9), (4, 9)], 16),
([(9, 2), (8, 2), (8, 3)], 9),
([(2, 1), (2, 2), (2, 3)], 10),
([(9, 3), (9, 4), (9, 5), (8, 5)], 22),
([(3, 2), (3, 3), (3, 4)], 18),
([(1, 7), (1, 8), (2, 8)], 12),
([(8, 1), (9, 1)], 16),
([(3, 6), (4, 6), (5, 6)], 12),
([(7, 3), (7, 2), (7, 1), (6, 1)], 17),
([(5, 1), (5, 2), (4, 2), (4, 1)], 23),
([(6, 8), (6, 7), (7, 7), (7, 6)], 21),
([(1, 5), (1, 4), (1, 3), (1, 2)], 14),
([(7, 5), (6, 5), (6, 6)], 24),
([(3, 8), (3, 7)], 9),
([(4, 8)], 7),
([(1, 6), (2, 6)], 15),
([(2, 4)], 8),
([(8, 4)], 4),
([(1, 1)], 6),
([(6, 2), (6, 3), (5, 3)], 8),
([(2, 7)], 2),
([(5, 5)], 2),
([(3, 9), (2, 9), (1, 9)], 22),
([(3, 1)], 3)
]

def killer_sudoku_solver(data):
    model = cp_model.CpModel()

    ORDEM = 9
    RAIZ = 3

    # cell[i][j] representa a célula na linha i e coluna j
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

    # restrição: cages 
    for cage in data:
        celulas, soma = cage
        vars_cage = []
        for (coluna, linha) in celulas:
            # converte para 0-based e (linha,coluna)
            v = (linha-1, coluna-1)
            vars_cage.append(cell[v])
        model.AddAllDifferent(vars_cage)
        model.Add(sum(vars_cage) == soma)

    # config solver
    solver = cp_model.CpSolver()

    # logs
    solver.parameters.log_search_progress = True
    solver.parameters.num_search_workers = 4  # paralelismo

    # solving the problem
    status = solver.Solve(model)

    # saída details
    print("="*50)

    if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
        if status == cp_model.OPTIMAL:
            print("\nSolução ótima encontrada! :D")
        else:
            print("\nSolução viável encontrada. :)")

        for i in range(ORDEM):
            if i % RAIZ == 0 and i != 0:
                print("-"*25)
            for j in range(ORDEM):
                if j % RAIZ == 0 and j != 0:
                    print("|", end=" ")
                print(f"{solver.Value(cell[(i,j)])} ", end=" ")
            print()
        
        print()

        # stats detalhadas
        print("\n" + "-"*50)
        print("ESTATÍSTICAS:")
        print(f"Status = {solver.status_name(status)}")
        print(f"Tempo de resolução: {solver.WallTime()} s")

        print(f"Conflitos: {solver.NumConflicts()}")
        print(f"Branches: {solver.NumBranches()}")
        print(f"Tempo de decisão: {solver.UserTime()}s")


        #print(f"Propagações: {solver.NumPropagations()}")
        #print(f"Variáveis no modelo: {model.NumVariables()}")
        #print(f"Restrições no modelo: {model.NumConstraints()}")



    else:
        print("\nNenhuma solução encontrada :/")
        print(f"Status: {solver.StatusName(status)}")
        print(f"Tempo de execução: {solver.WallTime():.2f} segundos")
        print(f"Conflitos: {solver.NumConflicts()}")
        print(f"Branches: {solver.NumBranches()}")


killer_sudoku_solver(generated)

#easy_data_1   medium_data_1    expert_data_1