#! /usr/bin/env python3
# credits: https://github.com/abidkyo/killer_sudoku_calc/tree/master

"""
Killer Sudoku Calculator Function.

Generate summands based on their sum with single-digit number only.

Feature:
- exclusion of digits
- inclusion of digits

Note: Summands is the number to be added
"""


def killer_sudoku_calc(sum, length=2, excl=None, incl=None):
    if length > 9:
        return []

    excl = [] if not excl else excl

    # Base case: length < 2.
    if length < 2:
        # Check for single-digit condition and excluded digit here.
        if 1 <= sum <= 9 and sum not in excl:
            return [(sum,)]
        else:
            return []

    incl = range(1, sum // length + 1) if not incl else incl
    # conjunto inicial de candidatos. 
    # higher bound pra evitar explorar números mt grandes

    res = []
    for i in incl:
        # skip number in exclude
        if i in excl:
            continue

        # add number to exlcude list
        excl.append(i)

        tmp = killer_sudoku_calc(sum - i, length=length - 1, excl=excl)

        # remove recently added number
        excl.pop()

        for j in tmp:
            # make the tuple and append to res
            summands = (i,) + j
            res.append(summands)

    # Filter is needed for len > 3 because duplicates are unavoidable
    res = sorted(list(set(map(tuple, map(sorted, res)))))

    return res