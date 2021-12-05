from aoc_cli import out, bcol, gate
import itertools
import copy

#day 5
def map_coordinates(user_input, variables):
    args = "src"
    diag = user_input.strip(" ")
    try:
        map = [[0 for x in range(1000)] for y in range(1000)]
        for line in variables[args]:
            bothcoords = line.split("-")
            start = bothcoords[0].split(",")
            end = bothcoords[1].split(",")
            start[0] = int(start[0].strip(" "))
            start[1] = int(start[1].strip(" "))
            end[0] = int(end[0].strip("> "))
            end[1] = int(end[1].strip(" "))
            if start[0] == end[0]:
                if start[1] <= end[1]:
                    while start[1] <= end[1]:
                        map[start[1]][start[0]] += 1
                        start[1] += 1
                else:
                    while start[1] >= end[1]:
                        map[start[1]][start[0]] += 1
                        start[1] -= 1
            elif start[1] == end[1]:
                if start[0] <= end[0]:
                    while start[0] <= end[0]:
                        map[start[1]][start[0]] += 1
                        start[0] += 1
                else:
                    while start[0] >= end[0]:
                        map[start[1]][start[0]] += 1
                        start[0] -= 1
            elif diag:
                if "true" != diag:
                    return out("Usage: map_coordinates <use diagonals=false or tue>", bcol.WARN)
                if start[0] <= end[0] and start[1] <= end[1]:
                    while start[1] <= end[1] or start[0] <= end[0]:
                        map[start[1]][start[0]] += 1
                        start[1] += 1
                        start[0] += 1
                elif start[0] >= end[0] and start[1] >= end[1]:
                    while start[0] >= end[0] or start[1] >= end[1]:
                        map[start[1]][start[0]] += 1
                        start[1] -= 1
                        start[0] -= 1
                elif start[0] <= end[0] and start[1] >= end[1]:
                    while start[0] <= end[0] or start[1] >= end[1]:
                        map[start[1]][start[0]] += 1
                        start[1] -= 1
                        start[0] += 1
                elif start[0] >= end[0] and start[1] <= end[1]:
                    while start[0] >= end[0] or start[1] <= end[1]:
                        map[start[1]][start[0]] += 1
                        start[1] += 1
                        start[0] -= 1
                else:
                    print(f"{start} -> {end}")
        res = 0
        with open("map.txt", 'w') as f:
            for col in map:
                for cell in col:
                    if cell == 0:
                        f.write("-")
                    elif cell <= 9:
                        f.write("" + str(cell))
                    elif cell <= 99:
                        f.write("" + str(cell))
                    if cell > 1:
                        res += 1
                f.write("\n")
        return out(f"There's {res} overlapping points", bcol.OKGREEN)
    except Exception as e:
        raise e
        return out(f"{e.__class__.__name__}: {e}", bcol.FAIL)
        

#day 4
def parse_bingo(user_input, variables):
    args = "src"
    try:
        res = []
        temp_list = []
        for item in variables[args][0].split(','):
            temp_list.append(int(item))
        c = 0
        for item in variables[args]:
            if c == 0:
                c += 1
            elif not item:
                res.append(temp_list.copy())
                temp_list.clear()
            else:
                small_list = []
                for num in item.split():
                    small_list.append(int(num))
                temp_list.append(small_list)
        variables[args] = res
        return f"{args} = {res}"
    except Exception as e:
        return out(f"{e.__class__.__name__}: {e}", bcol.FAIL)

def check_bingo(tables):
    for tab_i, table in enumerate(tables):
        if table:
            temp_col = [0] * 5
            for lin_i, line in enumerate(table):
                temp = 0
                for val_i, value in enumerate(line):
                    temp += value
                    temp_col[val_i] += value
                if temp == 0:
                    return table
            for val in temp_col:
                if val == 0:
                    return table
    return False

def check_bingo(table):
    if table:
        temp_col = [0] * 5
        for lin_i, line in enumerate(table):
            temp = 0
            for val_i, value in enumerate(line):
                if value != -1:
                    temp += value
                    temp_col[val_i] += value
            if temp == 0:
                return table
        for val in temp_col:
            if val == 0:
                return table
    return False

#day 4 2   
def solve_last_bingo(user_input, variables):
    args = "src"
    try:
        tables = copy.deepcopy(variables[args])
        extracted = tables.pop(0)
        for num in extracted:
            toremove = []
            for tab_i, table in enumerate(tables):
                for lin_i, line in enumerate(table):
                    for val_i, value in enumerate(line):
                        if value == num:
                            tables[tab_i][lin_i][val_i] = -1
                winning = check_bingo(table)
                if len(tables) == 1 and winning:
                    sum = 0
                    for resline in tables[0]:
                        for value in resline:
                            if value != -1:
                                sum += value
                    return out(f"sum: {sum} last value: {num} table index: {tab_i} multiplied: {sum * num}", bcol.OKGREEN)
                if len(tables) != 1 and winning:
                    toremove.append(winning)
            for l in toremove:
                tables.remove(l)
        return out(f"Can't resolve {tables}", bcol.FAIL)
    except Exception as e:
        return out(f"{e.__class__.__name__}: {e}", bcol.FAIL)

#day 4 1
def solve_bingo(user_input, variables):
    args = "src"
    try:
        tables = copy.deepcopy(variables[args])
        extracted = tables.pop(0)
        for num in extracted:
            for tab_i, table in enumerate(tables):
                for lin_i, line in enumerate(table):
                    for val_i, value in enumerate(line):
                        if value == num:
                            tables[tab_i][lin_i][val_i] = 0
                winning = check_bingo(table)
                if winning:
                    sum = 0
                    for line in winning:
                        for value in line:
                            sum += value
                    return out(f"sum: {sum} last value: {num} multiplied: {sum * num}", bcol.OKGREEN)
        return out(f"Can't resolve {tables}", bcol.FAIL)
    except Exception as e:
        return out(f"{e.__class__.__name__}: {e}", bcol.FAIL)

#day 3 2
def filter_commons(user_input, variables):    
    try:
        args = user_input.split()
        if len(args) < 1:
            return out("Usage: count_commons <src list>", bcol.WARN)
        args = args[0]
        if variables.get(args):
            copy1 = variables[args].copy()
            copy2 = variables[args].copy()
            index = 0
            while index < 12:
                ones = 0
                zeroes = 0
                for item in copy1:
                    if "0" in item[index]:
                        zeroes += 1
                    elif "1" in item[index]:
                        ones += 1
                new_list = []
                if zeroes <= ones:
                    for item in copy1:
                        if '1' == item[index]:
                            new_list.append(item)
                if zeroes > ones:
                    for item in copy1:
                        if '0' == item[index]:
                            new_list.append(item)
                copy1 = new_list.copy()
                if len(copy2) > 1:
                    new_list = []
                    ones = 0
                    zeroes = 0
                    for item in copy2:
                        if "0" in item[index]:
                            zeroes += 1
                        elif "1" in item[index]:
                            ones += 1
                    if zeroes <= ones:
                        for item in copy2:
                            if '0' == item[index]:
                                new_list.append(item)
                    if zeroes > ones:
                        for item in copy2:
                            if '1' == item[index]:
                                new_list.append(item)
                    copy2 = new_list.copy()
                index += 1
            return out(f"Result: {int(copy1[0], 2)}, not result: {int(copy2[0], 2)}, multiplied: {int(copy2[0], 2) * int(copy1[0], 2)}", bcol.OKGREEN)
        else:
            return out(f"Error: can't find {args}:<src list> in globals", bcol.FAIL)
    except Exception as e:
        return out(f"{e.__class__.__name__}: {e}", bcol.FAIL)
#day 3 1        
def count_commons(user_input, variables):
    try:
        args = user_input.split()
        if len(args) < 1:
            return out("Usage: count_commons <src list>", bcol.WARN)
        args = args[0]
        if variables.get(args):
            length = len(variables[args][0])
            ones = [0] * length
            zeroes = [0] * length
            for item in variables[args]:
                for i, char in enumerate(item):
                    if "0" in char:
                        zeroes[i] += 1
                    elif "1" in char:
                        ones[i] += 1
            final = ""
            for i in range(length):
                if ones[i] > zeroes[i]:
                    final += '1'
                else:
                    final += '0'
            val1 = int(final, 2)
            val2 = int(gate(final, 'not'), 2)
            return out(f"Multiplied result is: {val1 * val2}, decimal is: {val1}, not gate decimal is {val2}", bcol.OKGREEN)
        else:
            return out(f"Error: can't find {args}:<src list> in globals", bcol.FAIL)
    except Exception as e:
        return out(f"{e.__class__.__name__}: {e}", bcol.FAIL)

#day2
def find_arrive(user_input, variables):
    try:
        args = user_input.split()
        if len(args) <= 1:
            return out("Usage: find_arrive <src list> <use aim>:false or true", bcol.WARN)
        depth = 0
        aim = 0
        horizontal = 0
        if variables.get(args[0]):
            tar_list = variables[args[0]]
            if "false" in args[1]:
                for line in tar_list:
                    if "up" in line:
                        depth -= int(line.replace("up", ""))
                    elif "down" in line:
                        depth += int(line.replace("down", ""))
                    elif "forward" in line:
                        horizontal += int(line.replace("forward", ""))
            elif "true" in args[1]:
                for line in tar_list:
                    if "up" in line:
                        aim -= int(line.replace("up", ""))
                    elif "down" in line:
                        aim += int(line.replace("down", ""))
                    elif "forward" in line:
                        value = int(line.replace("forward", ""))
                        horizontal += value
                        depth += aim * value
            else:
                return out("Error: <use aim> can only be 'false' or 'true'", bcol.FAIL)
            return out(f"x is: {horizontal} depth is: {depth}, result is: {horizontal * depth}", bcol.OKGREEN)
        else:
            return out(f"Error: can't find {args[0]}:<src list> in globals", bcol.FAIL)
    except Exception as e:
        return out(f"{e.__class__.__name__}: {e}", bcol.FAIL)

# day1     
def find_increase(user_input, variables):
    try:
        args = user_input.split()
        if len(args) <= 1:
            return out("Usage: find_increase <src list> <window size>: 1 or 3", bcol.WARN)
        if variables.get(args[0]):
            window = int(args[1])
            if window == 3 or window == 1:
                max = 0
                tar_list = variables[args[0]]
                last = tar_list[0] if window == 1 else (tar_list[0] + tar_list[1] + tar_list[2])
                for i in itertools.count():
                    if i == 0: continue
                    if window == 1 and i == len(tar_list):
                        break
                    if window == 3 and i + 1 == len(tar_list):
                        break
                    val = tar_list[i] if window == 1 else (tar_list[i - 1] + tar_list[i] + variables[args[0]][i + 1])
                    if last < val:
                        max += 1
                    last = val
                else:
                    return out("Error: <window size> can only be 1 or 3", bcol.FAIL)
                return out(str(max), bcol.OKGREEN)
        else:
            return out(f"Error: can't find {args[0]}:<src list> in globals", bcol.FAIL)
    except Exception as e:
        return out(f"{e.__class__.__name__}: {e}", bcol.FAIL)

#2020 day 1
def findsum(user_input, variables):
    try:
        args = user_input.split()
        if len(args) <= 1:
                return out("Usage: findsum <target_value>:int <src list>", bcol.WARN)
        if variables.get(args[1]):
            value = int(args[0])
            for el in variables[args[1]]:
                if sum(el) == value:
                    return out(f"{el} sums to {value}", bcol.OKGREEN)
        else:
            return out(f"Error: can't find {args[1]}:<src list> in globals", bcol.FAIL)
    except Exception as e:
        return out(f"{e.__class__.__name__}: {e}", bcol.FAIL)