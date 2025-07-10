from ortools.sat.python import cp_model

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
            # Converte para 0-based e (linha,coluna)
            v = (linha-1, coluna-1)
            vars_cage.append(cell[v])
        model.AddAllDifferent(vars_cage)
        model.Add(sum(vars_cage) == soma)

    # Resolve o problema
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
        print("\nSolução encontrada :) !")
        for i in range(ORDEM):
            if i % RAIZ == 0 and i != 0:
                print("-"*25)
            for j in range(ORDEM):
                if j % RAIZ == 0 and j != 0:
                    print("|", end=" ")
                print(f"{solver.Value(cell[(i,j)])} ", end=" ")
            print()
        print()
        print(f"Status = {solver.status_name(status)}")

    else:
        print("\nNão tem solução :/")

easy_data_1 = [
    #BLOCO 1
    ([(1,1),(1,2)],15), #coluna / linha
    ([(2,1)],1),
    ([(2,2)],8),
    ([(1,3),(2,3)],7), #coluna / linha
    ([(3,1),(4,1),(5,1)],12), #coluna / linha
    ([(3,2),(4,2)],12), #coluna / linha
    ([(3,3),(4,3),(4,4)],8), #coluna / linha
    #BLOCO 1

    #BLOCO 2
    ([(5,2),(5,3),(5,4)],16),
    ([(6,1),(7,1),(8,1),(7,2)],18),
    ([(6,2),(6,3),(7,3)],16),
    #BLOCO 2

    #BLOCO 3
    ([(9,1)],8),
    ([(8,2),(9,2)],6),
    ([(8,3),(8,4),(9,3),(9,4)],24),
    #BLOCO 3

    #BLOCO 4
    ([(1,4),(2,4),(2,5),(1,5),(1,6)],31),
    ([(3,4)],5),
    ([(3,5),(3,6),(2,6)],9),
    #BLOCO 4

    #BLOCO 5
    ([(6,4),(6,5)],10),
    ([(4,5),(5,5)],11),
    ([(4,6),(5,6),(5,7)],16),
    ([(6,6),(6,7),(7,7)],10),
    #BLOCO 5

    #BLOCO 6
    ([(7,4)],9),
    ([(7,5),(7,6)],12),
    ([(8,5),(9,5),(9,6),(9,7)],16),
    ([(8,6),(8,7),(8,8),(9,8)],20),
    #BLOCO 6

    #BLOCO 7
    ([(1,7),(2,7),(3,7),(4,7)],22),
    ([(1,8),(2,8)],7),
    ([(1,9),(2,9)],8),
    ([(3,8),(4,8),(5,8)],19),
    ([(3,9),(4,9)],12),
    #BLOCO 7

    #BLOCO 8
    ([(5,9),(6,9)],13),
    ([(6,8),(7,8)],12),
    #BLOCO 8

    #BLOCO 9
    ([(7,9),(8,9)],3),
    ([(9,9)],9),
    #BLOCO 9
]


medium_data_1 = [
    #BLOCO 1
    ([(1,1),(1,2),(1,3)],6), #coluna / linha
    ([(2,1),(3,1),(2,2),(3,2),(2,3)],35),
    ([(3,3),(4,3)],10),
    #BLOCO 1

    #BLOCO 2
    ([(4,1),(4,2)],7), 
    ([(5,1),(5,2)],7), 
    ([(5,3),(5,4)],16), #coluna / linha
    ([(6,1),(7,1),(8,1)],21), 
    ([(6,2),(7,2)],9),
    ([(6,3),(7,3),(6,4),(7,4)],20), 
    #BLOCO 2

    #BLOCO 3
    ([(9,1),(9,2),(8,2)],15),
    ([(8,3),(9,3),(9,4)],10),
    #BLOCO 3

    #BLOCO 4
    ([(1,4)],4),
    ([(2,4),(3,4),(3,5)],9),
    ([(1,5),(2,5)],13),
    ([(1,6),(2,6),(2,7)],18),
    ([(3,6),(4,6)],9),
    #BLOCO 4

    #BLOCO 5
    ([(4,4),(4,5)],17),
    ([(5,5),(6,5)],6),
    ([(5,6),(6,6)],11),
    #BLOCO 5

    #BLOCO 6
    ([(8,4),(8,5),(7,5)],15),
    ([(7,6),(7,7)],8),
    ([(8,6),(8,7)],10),
    ([(9,5),(9,6),(9,7)],10),
    #BLOCO 6

    #BLOCO 7
    ([(1,7)],6),
    ([(1,8),(1,9),(2,9)],17),
    ([(2,8),(3,8)],4),
    ([(3,7),(4,7)],6),
    ([(3,9),(4,9)],12),
    #BLOCO 7

    #BLOCO 8
    ([(5,7),(5,8),(4,8)],20),
    ([(5,9),(6,9)],7),
    ([(6,7),(6,8),(7,8)],17),
    #BLOCO 8

    #BLOCO 9
    ([(7,9),(8,9)],10),
    ([(8,8)],4),
    ([(9,8),(9,9)],16),
    #BLOCO 9

]

killer_sudoku_solver(medium_data_1)