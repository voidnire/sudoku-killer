import random

# Constante para o tamanho do grid (padrão 9x9)
GRID_SIZE = 9

def print_grid(grid):
    """Função para imprimir o grid de Sudoku de forma legível."""
    for row in range(GRID_SIZE):
        if row % 3 == 0 and row != 0:
            print("- - - - - - - - - - - - ")
        for col in range(GRID_SIZE):
            if col % 3 == 0 and col != 0:
                print(" | ", end="")
            print(grid[row][col], end=" ")
        print()

def find_empty_cell(grid):
    """Encontra a próxima célula vazia (com valor 0) no grid."""
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == 0:
                return (i, j)  # Retorna a tupla (linha, coluna)
    return None

def is_valid(grid, num, pos):
    """
    Verifica se um número é válido em uma determinada posição, de acordo com as regras do Sudoku.
    'pos' é uma tupla (linha, coluna).
    """
    row, col = pos

    # Checa a linha
    for i in range(GRID_SIZE):
        if grid[row][i] == num and col != i:
            return False

    # Checa a coluna
    for i in range(GRID_SIZE):
        if grid[i][col] == num and row != i:
            return False

    # Checa o bloco 3x3
    box_x = col // 3
    box_y = row // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if grid[i][j] == num and (i, j) != pos:
                return False

    return True

def solve_attempt(grid):
    """
    Tenta resolver o Sudoku usando backtracking recursivo com escolhas aleatórias.
    Esta é a parte tática de uma única "aposta".
    """
    find = find_empty_cell(grid)
    if not find:
        return True  # Se não há células vazias, o Sudoku está completo e resolvido.
    else:
        row, col = find

    # --- aleatoriedade ---
    numbers_to_try = list(range(1, GRID_SIZE + 1))
    random.shuffle(numbers_to_try) # Embaralha os números a serem tentados

    for num in numbers_to_try:
        if is_valid(grid, num, (row, col)):
            grid[row][col] = num

            # Chama a recursão para preencher o resto do grid
            if solve_attempt(grid):
                return True

            # Se a recursão falhou, desfaz a jogada (backtrack)
            grid[row][col] = 0
            
    # Se nenhum número funcionou, esta tentativa falhou.
    return False

def generate_sudoku():
    """
    Função principal que implementa a estratégia do Algoritmo de Las Vegas.
    Ele continuará tentando resolver um grid do zero até que tenha sucesso.
    """
    attempts = 0
    while True:
        attempts += 1
        print(f"Tentativa de geração nº {attempts}...")
        
        # Cria um grid vazio a cada nova tentativa
        grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        # Tenta preencher o grid. Se conseguir, a "aposta" foi ganha.
        if solve_attempt(grid):
            print(f"\nSucesso! Grid de Sudoku válido gerado na tentativa {attempts}.")
            return grid
        # Se solve_attempt retornar False, o loop continua e tudo recomeça.
