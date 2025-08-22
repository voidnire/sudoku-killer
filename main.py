from puzzle_generation.sudoku_gen import *
from grid_to_image import *
import os

# garante que a pasta existe
os.makedirs("generated", exist_ok=True)

# define o caminho completo do arquivo
outfile = os.path.join("generated", "sudoku.png")
# chama a função

sudoku_grid = generate_sudoku()
#print("-" * 25)
#print("Grid de Sudoku Gerado:")
#print("-" * 25)
#print_grid(sudoku_grid)

render_sudoku(sudoku_grid,outfile=outfile)
