from ortools.sat.python import cp_model


def create_sudoku_model(n,X):
    N = n * n
    model = cp_model.CpModel()


    # variáveis
    for i in range(N):
        for j in range(N):
            X[(i,j)] = model.NewIntVar(1, N, f'X_{i}_{j}')

    # linhas
    for i in range(N):
        model.AddAllDifferent([X[(i,j)] for j in range(N)])

    # colunas
    for j in range(N):
        model.AddAllDifferent([X[(i,j)] for i in range(N)])

    #  blocos
    for bi in range(n):
        for bj in range(n):
            block_cells = []
            for i in range(n):
                for j in range(n):
                    block_cells.append(X[(bi*n + i, bj*n + j)])
            model.AddAllDifferent(block_cells)

    for b in range(len(block_cells)):
        print(block_cells[b])
    

    return model, X, N

def print_sol(n, solver, status, X, N):
    print()
    print(f"EXEMPLO {n} x {n}")
    
    print(f'Status: {solver.StatusName(status)}')

    print()
    if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
        for i in range(N):
            print([solver.Value(X[(i,j)]) for j in range(N)])
    else:
        print('Sem solução!')
    print()


def main():
    n = 2  # Sudoku 4x4 tem blocos 2x2
    X = {}

    model, X, N =  create_sudoku_model(n,X)
    gaiolas2 = {
        X[(0,0)] + X[(0,1)] == 5,
        X[(1,0)] + X[(2,0)] == 6,
        X[(1,0)] + X[(2,0)] == 6,
        X[(3,0)] + X[(3,1)] == 5,
        X[(0,2)] + X[(1,2)] + X[(1,1)] == 7,
        X[(0,3)] + X[(1,3)] == 4,
        X[(2,3)] + X[(3,3)] + X[(3,2)] == 9
    }

    for cage in gaiolas2:
        model.Add(cage)

    #resolver e imprimir
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    print_sol(n, solver, status, X, N)


    n = 3  # SUDOKU 3x3
    X = {}
    model2, X, N =  create_sudoku_model(n,X)
    gaiolas3 = {
        X[(0,0)] + X[(0,1)] == 7,
        X[(0,2)] + X[(0,3)] == 12,
        X[(0,5)] + X[(0,6)] == 5,
        X[(0,7)] + X[(0,8)] == 12,

        #adiçoes... de celulas sem cages
        X[(0,4)] ==9,
        X[(1,2)] ==2,
        X[(2,6)] ==6,
        X[(5,1)] ==2,
        X[(7,6)] ==5,
        X[(4,7)] ==1,
        X[(8,1)] ==9,
        X[(8,4)] ==4,

        X[(1,0)] + X[(2,0)] == 9,
        X[(1,1)] + X[(2,1)] + X[(2,2)] == 19,
        X[(1,3)] + X[(2,3)] == 9,
        X[(1,4)] + X[(2,4)] == 13,
        X[(1,5)] + X[(2,5)] == 7,
        X[(1,6)] + X[(1,7)]+ X[(2,7)] == 15,
        X[(1,8)] + X[(2,8)] == 10,

        X[(3,0)] + X[(3,1)] == 10,
        X[(3,2)] + X[(3,3)] == 10,
        X[(3,5)] + X[(3,6)] == 12,
        X[(3,7)] + X[(3,8)] == 8,

        
        X[(4,0)] + X[(5,0)] == 14,
        X[(4,1)] + X[(4,2)] + X[(5,2)]== 12,
        X[(4,3)] + X[(5,3)] == 9,
        X[(4,4)] + X[(5,4)] == 9,


        X[(4,5)] + X[(5,5)] == 15,
        X[(4,6)] + X[(5,6)] + X[(5,7)] == 20,
        X[(4,8)] + X[(5,8)] == 8,

        X[(6,0)] + X[(6,1)] == 6,
        X[(6,2)] + X[(6,3)] == 11,
        X[(6,4)] + X[(7,4)] == 5,
        X[(6,5)] + X[(6,6)] == 10,
        X[(6,7)] + X[(6,8)] == 15,

        X[(7,0)] + X[(8,0)] == 10,
        X[(7,1)] + X[(7,2)] + X[(8,2)]== 15,
        X[(7,3)] + X[(8,3)] == 14,
        X[(7,5)] + X[(8,5)] == 15,
        X[(7,7)] + X[(8,7)] + X[(8,6)] == 10,
        X[(8,7)] + X[(8,8)] == 6
        }
    for cage in gaiolas3:
        model2.Add(cage)

    #resolver e imprimir
    solver = cp_model.CpSolver()
    status = solver.Solve(model2)

    print_sol(n, solver, status, X, N)
    print()


if __name__ == '__main__':
    main()