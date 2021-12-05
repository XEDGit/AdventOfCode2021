import enum
import itertools
import os
import signal
import sys
import platform
import subprocess
import copy
from days import *
try:
    import getch
except:
    import msvcrt as getch

class bcol:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#generator functions
def gettype(user_input):
    if 'int' in user_input:
        return int
    if 'str' in user_input:
        return str

def evaluate_input(user_input):
    try:
        compile(user_input, '<stdin>', 'eval')
    except:
        return exec
    else:
        return eval

#utility functions
def out(msg, col):
    return f"{col}{msg}{bcol.ENDC}"

def terminate(signum=0, err=0):
    print(out(f"{bcol.BOLD}Goodbye!♥", bcol.OKGREEN))
    os.remove("stdout_temp.txt")
    exit()
    
def gate(input, gatename):
    if "not" in gatename:
        output = ""
        for ch in input:
            if "1" in ch:
                output += '0'
            elif "0" in ch:
                output += '1'
        return output
    else:
        print("Gate not supported")        

def get_input():
    if "Windows" in platform.platform():
        res = getch.getch()
    else:
        res = bytes(getch.getche(), encoding="utf-8")
    if b'\x03' in res or b'\x04' in res:
        terminate()
    return res
    
def streach(args):
    res = " "
    for arg in args.split():
        res += str(arg)
        res += " "
    res = res[:-1]
    return res

#custom user functions
def group(user_input, variables):
    args = user_input.split()
    if len(args) <= 2:
            return out("Usage: group <groups dimesion>:int <new variable name>:str <source variable>:str", bcol.WARN)
    if "all" in args[0]:
        if len(args) >= 4:
            if variables.get(args[3]):
                value = int(args[1])
                new_list = list(itertools.combinations(variables[args[3]], value))
                variables[args[2]] = new_list
            else:
                return out(f"Error: can't find {args[1]}:<src list> in globals", bcol.FAIL)
        else:
            return out("Usage: group all <groups dimesion>:int <new variable name>:str <source variable>:str", bcol.WARN)
    else:
        if not variables.get(args[2]):
            return out(f"Error: '{args[2]}' not found in global variables", bcol.FAIL)
        new_list = []
        value = int(args[0])
        for x in range(0, len(variables[args[2]]), value):
            new_list.append(variables[args[2]][x:x+value])
        variables[args[1]] = new_list
    return new_list

def parseday(user_input, variables):
    args = user_input.split()
    if len(args) < 1:
        return out("Usage: parseday <day>:int <data type>:'int' or 'str' or 'dlist or 'dict'", bcol.WARN)
    file_path = "inputs/" + args[0]
    if ".txt" not in file_path:
        file_path += ".txt"
    try:
        fd = open(file_path, 'r')
    except:
        return out(f"Error: File '{file_path}' not found", bcol.FAIL)
    if len(args) < 2:
        return out("Usage: parseday <day>:int <data type>:'int' or 'str' or 'dlist or 'dict'", bcol.WARN)
    if "str" in args[1] or "int" in args[1]:
        values = []
        typ = gettype(args[1])
        for line in fd.readlines():
            try:
                if typ == str:
                    values.append(typ(line).rstrip("\n"))
                else:
                    values.append(typ(line))
            except:
                return out("Error: data type not compatible", bcol.FAIL)
    elif "dlist" in args[1]:
        values = []
        new_dict = {}
        for i, line in enumerate(fd.readlines()):
            items = line.split()
            if len(items) == 0:
                values.append((new_dict))
                new_dict.clear()
                continue
            for item in items:
                dict_vals = item.split(':')
                if len(dict_vals) != 2:
                    return out(f"Error: found a value not parsable to dictionary at line {i + 1}", bcol.FAIL)
                new_dict[dict_vals[0]] = dict_vals[1]
    elif "dict" in args[1]:
        values = {}
        for i, line in enumerate(fd.readlines()):
            dict_vals = line.split(':')
            if len(dict_vals) != 2:
                return out(f"Error: found a value not parsable to dictionary at line {i + 1}", bcol.FAIL)
            values[dict_vals[0]] = dict_vals[1]
    else:
        return out("Error: <data type> must be 'int' or 'str' or 'dlist' or 'dict'", bcol.FAIL)
    variables["src"] = values
    fd.close()
    return f"src = {values}"
#main loop functions
def execute_custom_bash(user_input, command):
    with open("stdout_temp.txt", 'w+') as f:
        subprocess.run(f"{command}{streach(user_input)}", shell=True, stdout=f, stderr=f)
        f.close()
        f = open("stdout_temp.txt", 'r')
        res = f.read()[:-1]
        f.close()
    if not res:
        res = "Success!"
    return res 
    
def execute_input(user_input, variables, custom_bash, custom_funcs, sim):
    res = ""
    stdout = ""
    #custom bash iteration
    for key in custom_bash:
        if key in user_input:
            res = execute_custom_bash(user_input.replace(key, ""), custom_bash[key]) if sim == False else "User-defined bash method"
            return res , stdout
    #custom func iteration
    for key in custom_funcs:
        if key in user_input:
            res = custom_funcs[key](user_input.replace(key, ""), variables)
            return res, stdout
    #normal python exec or eval
    evaluated_func = evaluate_input(user_input)
    f = open("stdout_temp.txt", 'w+')
    temperr = sys.stderr
    tempout = sys.stdout
    sys.stdout = f
    sys.sterr = f
    try:
        res = evaluated_func(user_input, variables)
    except Exception as e:
        res = f"{e.__class__.__name__}: {e}"
    sys.stdout = tempout
    sys.stderr = temperr
    f.close()
    f = open("stdout_temp.txt", 'r')
    stdout = f.read()[:-1]
    f.close()
    return str(res), stdout

def concat_functions(user_input, variables, custom_bash, custom_funcs, sim=False):
    args = user_input.split('|')
    res = ""
    out_len = variables["OUT_LEN"]
    for i, cmd in enumerate(args):
        if i > 0:
            res += '\n'
        if i > 0 and sim:
            res += "      "
        if len(args) >= 2:
            res += f"[pipe {i}]: "
        tres, tstdout = execute_input(cmd.lstrip(), variables, custom_bash, custom_funcs, sim)
        if tres and 'None' not in tres:
            res += f"{str(tres)[0:out_len]}{'...' if len(tres) > out_len else ''}"
        if tstdout:
            res += tstdout
    return res


def main():
    custom_bash = {
        "getday" :	f"{sys.executable} ./customs.py getday",
        "foo" :		f"{sys.executable} ./customs.py foo",
        "rm" :		rm_keyword,
        "cat" :     cat_keyword
              }
    custom_funcs = {
        "group" :			    group,
        "parseday" :		    parseday,
        "findsum" :			    findsum,
        "find_increase" :	    find_increase,
        "find_arrive" :		    find_arrive,
        "count_commons" :       count_commons,
        "filter_commons" :      filter_commons,
        "parse_bingo" :         parse_bingo,
        "solve_bingo" :         solve_bingo,
        "solve_last_bingo" :    solve_last_bingo,
        "map_coordinates" :     map_coordinates,
        "2020 day 1" :			findsum,
        "day 1" :       	    find_increase,
        "day 2" :		        find_arrive,
        "day 3 1" :             count_commons,
        "day 3 2" :             filter_commons,
        "day 4 1" :             solve_bingo,
        "day 4 2" :             solve_last_bingo,
        "day 5" :               map_coordinates
    }
    variables = {
        "OUT_LEN" : 150,
        }
    history = [
            f"{bcol.BOLD}{bcol.OKGREEN}Welcome to aoc_CLI from XEDGit",
            f"{bcol.OKBLUE}Enviromental variables(current value):",
            f"\t{bcol.OKBLUE}OUT_LEN(150) = length of output before being truncated",
            f"{bcol.WARN}Use '{bytes.decode(up_key)}' or '{bytes.decode(down_key)}' to access command history!",
            bcol.ENDC
            ]
    cmd_history = [
        "OUT_LEN = "
    ]
    cmd_index = 0
    autocomplete_index = 0
    user_input = ""
    ch = ''
    byte = b''
    compatibles = []
    subprocess.run(clear_keyword, shell=True)
    while 1:
        #print interface
        his_max_len = os.get_terminal_size(1)[1] - 2
        his_len = len(history)
        for i, el in enumerate(history):
            if i > his_len - his_max_len:
                print(el)
        print(f"{bcol.BOLD}{bcol.OKCYAN}☃ aoc@$hell~>{bcol.ENDC} {user_input}")
        #print autocomplete commands on tab
        if tab in byte and compatibles:
            for cmd in compatibles:
                print(cmd)
        #print all available funcs on help
        elif "help" in user_input:
            print(f"{bcol.WARN}Available bash commands:{bcol.ENDC}")
            for i, item in enumerate(custom_bash):
                print(out(item, bcol.UNDERLINE), end="   ")
                if i % 6 == 5:
                    print('')
            print(f"{bcol.WARN}\nAvailable functions:{bcol.ENDC}")
            for i, item in enumerate(custom_funcs):
                if "day" in item:
                    i = 0
                if "2020" in item:
                    print(out("\nAbbreviations by day:", bcol.WARN))
                print(out(item, bcol.UNDERLINE), end="   ")
                if i % 6 == 5:
                    print('')
            print('')
        #print simulated output
        if user_input:
            res = concat_functions(user_input, copy.deepcopy(variables), custom_bash, custom_funcs, True)
            if res:
                print(f"{bcol.BOLD}{bcol.WARN}Out~> {bcol.ENDC}{res}")
        #get user input
        byte = get_input()
        try:
            ch = bytes.decode(byte)
        except:
            ch = ''
        subprocess.run(clear_keyword, shell=True)
        #check for special keys
        #enter
        if enter in byte:
            autocomplete_index = 0
            history.append(f"{bcol.BOLD}{bcol.OKCYAN}☃ aoc@$hell~>{bcol.ENDC} {user_input}")
            if cmd_index > 0:
                cmd_index = 0
                cmd_history.pop(0)
            if user_input:
                cmd_history.insert(0, user_input)
            res = concat_functions(user_input, variables, custom_bash, custom_funcs,)
            user_input = ""
            if res:
                history.append(res)
        #backspace
        elif backspace in byte:
            user_input = user_input[:-1]
        #autocomplete
        elif tab in byte:
            if user_input:
                compatibles = []
                for func in custom_funcs:
                    if user_input[0] in func[0]:
                        compatibles.append(func)
                if compatibles:
                    user_input = compatibles[autocomplete_index]
                    compatibles[autocomplete_index] = out(compatibles[autocomplete_index], bcol.OKGREEN)
                    autocomplete_index += 1
                    if autocomplete_index == len(compatibles):
                        autocomplete_index = 0
        #command history handling
        elif up_key in byte and cmd_index + 1 < len(cmd_history):
            if cmd_index == 0:
                cmd_history.insert(0, user_input)
            cmd_index += 1
            user_input = cmd_history[cmd_index]
        elif down_key in byte and cmd_index > 0:
            cmd_index -= 1
            user_input = cmd_history[cmd_index]
            if cmd_index == 0:
                cmd_history.pop(0)
        #normal case handling
        elif ch:
            user_input += ch

#Start of program
signal.signal(signal.SIGINT, terminate)

#Defining system dependant globals
up_key = b'`'
down_key = b'~'
if "Windows" in platform.platform():
    rm_keyword = "del"
    clear_keyword = "cls"
    cat_keyword = "type"
    backspace = b'\x08'
    enter = b'\r'
    tab = b'\t'
else:
    rm_keyword = "rm"
    clear_keyword = "clear"
    cat_keyword = "cat"
    backspace = b'\x7f'
    enter = b'\n'
    tab = b'\t'

if (__name__ == "__main__"):
    main()