#!/usr/bin/env python3
# Copyright 2010-2025 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START program]
"""Simple solve."""
# [START import]
from ortools.sat.python import cp_model
# [END import]


def main() -> None:
    """Minimal CP-SAT example to showcase calling the solver."""
    # Creates the model.
    # [START model]
    model = cp_model.CpModel()
    # [END model]
    grid={}
    dimension = 4
    # Creates the variables.
    # [START variables]

    for x in range(dimension):
        for y in range(dimension):
            for z in range(dimension):
                grid[x,y,z] = model.NewBoolVar(f'grid_{x}_{y}_{z}')

    #var_upper_bound = max(3, 3, 3)
    #x = model.new_int_var(0, var_upper_bound, "x")
    #y = model.new_int_var(0, var_upper_bound, "y")
    #z = model.new_int_var(0, var_upper_bound, "z")
    # [END variables]

    # Creates the constraints.
    # [START constraints]

    # each cell has exactly one value
    for x in range(dimension):
        for y in range(dimension):
            model.AddExactlyOne(grid[x,y,z] for z in range(dimension))

    # each value appears one time on col & line & block
    for z in range(dimension):
        for x in range(dimension):
            model.AddExactlyOne(grid[x,y,z] for y in range(dimension))#linha
    for z in range(dimension):
        model.AddExactlyOne(grid[x,y,z] for x in range(dimension))#coluna

        block_size = 2
    for z in range(dimension):
        for block_x in range(0, dimension, block_size):
            for block_y in range(0, dimension, block_size):
                cells = []
                for dx in range(block_size):
                    for dy in range(block_size):
                        x = block_x + dx
                        y = block_y + dy
                        cells.append(grid[x, y, z])
                model.AddExactlyOne(cells)



    # [END constraints]

    # [START objective]
    model.maximize(2 * x + 2 * y + 3 * z)
    # [END objective]

    # Creates a solver and solves the model.
    # [START solve]
    solver = cp_model.CpSolver()
    status = solver.solve(model)
    # [END solve]

    # [START print_solution]
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f"Maximum of objective function: {solver.objective_value}\n")
        print(f"x = {solver.value(x)}")
        print(f"y = {solver.value(y)}")
        print(f"z = {solver.value(z)}")
    else:
        print("No solution found.")
    # [END print_solution]

    # Statistics.
    # [START statistics]
    print("\nStatistics")
    print(f"  status   : {solver.status_name(status)}")
    print(f"  conflicts: {solver.num_conflicts}")
    print(f"  branches : {solver.num_branches}")
    print(f"  wall time: {solver.wall_time} s")
    # [END statistics]


if __name__ == "__main__":
    main()
# [END program]