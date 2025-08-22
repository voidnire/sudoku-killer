import random
# based on Killer Sudoku Calculator Function
# generates complete solved sudoku w/ backtracking
# divide cages in random sizes 2-4
N = 9

def is_valid(board, row, col, num):
    """Verifica se pode colocar num na posição (row, col)."""
    for i in range(N):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = (row // 3) * 3, (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def solve_board(board):
    """Backtracking para gerar uma solução completa de Sudoku."""
    for row in range(N):
        for col in range(N):
            if board[row][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_board(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_full_solution():
    board = [[0 for _ in range(N)] for _ in range(N)]
    solve_board(board)
    return board

def generate_cages(board):
    """Divide o tabuleiro em cages com soma baseada na solução."""
    cells = [(r, c) for r in range(N) for c in range(N)]
    random.shuffle(cells)
    cages = []
    visited = set()

    while cells:
        r, c = cells.pop()
        if (r, c) in visited:
            continue
        size = random.choice([2, 3, 4])  # tamanho da cage
        cage = [(r, c)]
        visited.add((r, c))

        # cresce a cage aleatoriamente
        for _ in range(size - 1):
            neighbors = [(r+dr, c+dc) for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]
                         if 0 <= r+dr < N and 0 <= c+dc < N and (r+dr, c+dc) not in visited]
            if not neighbors:
                break
            nr, nc = random.choice(neighbors)
            cage.append((nr, nc))
            visited.add((nr, nc))
            r, c = nr, nc

        # soma real da cage
        soma = sum(board[rr][cc] for rr, cc in cage)
        cages.append({"cells": cage, "sum": soma})

    return cages

def print_solution_with_cages(solution, cage_labels):
    print("\n=== Solução com Gaiolas ===")
    for r in range(N):
        row_str = ""
        for c in range(N):
            val = solution[r][c]
            label = cage_labels[r][c]
            row_str += f"{val}{label:>2} "
        print(row_str)


if __name__ == "__main__":
    solution = generate_full_solution()
    cages = generate_cages(solution)

    print("Solução completa:")
    for row in solution:
        print(row)

    print("\nCages gerados:")
    for cage in cages:
        print(cage)

# IMPROVEMENT POINTS
# Garantir que cada cage seja realmente contígua 
# (hoje pode formar uns formatos estranhos).

#Implementar verificação de unicidade da solução 
# (às vezes a geração pode permitir múltiplas soluções).

# Controlar melhor variação de dificuldade 
# (usando heurísticas de “solvabilidade”).