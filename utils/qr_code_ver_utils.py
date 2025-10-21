# TODO: remove this utils file when finished with SPIKE user story 
#       (i'm offline now, can't remember which one)


from . import qr_utils
import math


def print_qr_code_version_sizes():
    print("version | rows | columns | odd number of rows? | odd number of columns?")

    for i in range(1, 41):
        rows, cols = qr_utils.temp_get_qr_matrix(i)
        version_cell = f"{i}".ljust(7, ' ')
        rows_cell = f"{rows}".ljust(4, ' ')
        cols_cell = f"{cols}".ljust(7, ' ')
        odd_rows_cell = f"{rows % 2 == 1}".ljust(19, ' ')
        odd_cols_cell = f"{cols % 2 == 1}".ljust(21, ' ')
        print(f"{version_cell} | {rows_cell} | {cols_cell} | {odd_rows_cell} | {odd_cols_cell}")


def get_lcm(nums: list[int]) -> int:
    result = math.lcm(*nums)
    return result
