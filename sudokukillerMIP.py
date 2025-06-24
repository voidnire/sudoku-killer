import gurobipy as gp

data_killer = [
    ([(1,1),(1,2)],15),
    ([(2,1),(2,2)],8),
    ([(3,1),(3,2)],3),
    ([(4,1),(5,1)],16),
    ([(6,1),(7,1)],5),
    ([(8,1),(9,1),(8,2),(9,2)],24),
    ([(4,2),(3,3),(3,4),(4,3)],18),
    ([(5,2),(5,3),(5,4),(5,5),(5,6)],25),
    ([(6,2),(6,3)],5),
    ([(7,2),(7,3)],7),
    ([(1,3),(1,4),(1,5),(1,6)],22),
    ([(2,3),(2,4)],5),
    ([(8,3),(9,3)],12),
    ([(4,4),(4,5)],9),
    ([(6,4),(7,4),(8,4)],18),
    ([(9,4),(9,5)],14),
    ([(2,5),(3,5),(3,6),(4,6)],24),
    ([(6,5),(6,6)],16),
    ([(7,5),(7,6),(8,5),(8,6)],14),
    ([(2,6),(1,7),(2,7),(1,8),(1,9)],21),
    ([(9,6),(9,7)],10),
    ([(3,7),(4,7)],17),
    ([(5,7),(6,7),(7,7),(8,7)],11),
    ([(2,8),(2,9)],11),
    ([(3,8),(3,9)],11),
    ([(4,8),(4,9)],9),
    ([(5,8),(5,9),(6,9),(7,9)],22),
    ([(6,8),(7,8)],15),
    ([(8,8),(9,8)],9),
    ([(8,9),(9,9)],9),
]

# checando se ta certo as cages ---------------------------------
for squares, sum_ in data_killer[6:9]:
    print(f"Sum of cells marked below must add up to {sum_}")
    out = ""
    for x in range(1,10):
        for y in range(1,10):
            out += "x" if (y,x) in squares else "."
        out += "\n"
    print(out)
    print()
# checando se ta certo as cages ---------------------------------

# checando se cada celula esta em exatamente 1 grupo ------------------------
sqs = set()
for squares, sum_ in data_killer:
    for s in squares:
        assert s not in sqs, "Repeated killer square"
        sqs.add(s)
# checando se cada celula esta em exatamente 1 grupo ------------------------


# estabelecendo regra de cada grupo contém os números de 1 a 9 exatamente 1 vez ----------------
data_sudoku = []
for x in range(1,10,3):
    for y in range(1,10,3):
        data_sudoku.append([(x+i,y+j) for i in range(3) for j in range(3)])

for q in range(1,10):
    data_sudoku.append([(q,w) for w in range(10)])
    data_sudoku.append([(w,q) for w in range(10)])

# checando a regra
for squares in data_sudoku[:2]:
    out = ""
    for x in range(1,10):
        for y in range(1,10):
            out += "x" if (y,x) in squares else "."
        out += "\n"
    print(out)
    print()

# estabelecendo regra de cada grupo contém os números de 1 a 9 exatamente 1 vez ----------------


# CONSTRUINDO MODELO MIP CONSTRUINDO MODELO MIP CONSTRUINDO MODELO MIP
m = gp.Model()
