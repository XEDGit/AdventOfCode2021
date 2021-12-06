#Welcome to aoc_CLI for Advent of Code 2021!
This small project points towards making command line interface
with python, where you can use **python**, **bash** and **user-made functions**, with the
scope of helping during the AoC

It features **live output**, **autocomplete** and **command history managing**

##Custom functions

So I guess you're now thinking what kind of functions are in there, and as you
can imagine there's functions for **downloading**, **parsing** and **solving** the daily
challenges obviously!

Here's a list:

###Functions:
    -group : used to regroup src in various ways
    -parseday : used to parse a input file to a local variable
    -findsum : 2020 day 1 solve
    -find_increase : day 1 solve 
    -find_arrive : day 2 solve
    -count_commons : day 3 part 1 solve
    -filter_commons : day 3 part 2 solve
    -parse_bingo : parse "src" as bingo boards, use before solve_bingo or next
    -solve_bingo : day 4 part 1 solve
    -solve_last_bingo : day 4 part 2 solve
    -map_coordinates : day 5 solve

###Day shortcuts:
    -2020 day 1 
    -day 1
    -day 2
    -day 3 1
    -day 3 2
    -day 4 1
    -day 4 2
    -day 5

###Bash command:
    -getday <day>: downloads a day's input from adventofcode.com
    -foo : you should't try it
    -rm <path>: removes a file
    -cat <path>: shows content of a text file located into /inputs folder
    
    remember the file path on Windows is with \ in UNIX with /

If you don't remember this list **you can always type "help" into the CLI**, if
instead **you need help with the command usage, try typing the command itself**, the
CLI will provide you with arguments explaination

To **navigate your command history** use the keys '`' for moving back and '~' for forward

To **use autocomplete** simply type part of the desired command, and then click 'TAB'

Enviromental variable(Default value):
    -OUT_LEN(150): length of output before being truncated