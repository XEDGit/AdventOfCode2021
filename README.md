# Welcome to CLI for Advent of Code 2021!
This small project points towards making command line interface
with python, where you can use **python**, **bash** and **user-made functions**, with the
scope of helping during the AoC

It features **live output**, **autocomplete** and **command history managing**

## Info:

### Dependencies:
   - python3

### Platform:

  - 🍏 <img src="https://img.shields.io/badge/MacOs-working-brightgreen" />

  - 🐧 <img src="https://img.shields.io/badge/Linux-working-brightgreen" />

  - 🪟 <img src="https://img.shields.io/badge/Windows-working-brightgreen" />

## Setup:
### Terminal and Powershell

      git clone git@github.com:XEDGit/aoc_CLI.git
      cd aoc_CLI/
      python3 aoc_CLI.py
      getday 6
      
Now fill the cookie.txt new created file with your session id from advent of code website and run
      
      getday 6
      parseday 6 int ,
      day 6
      
There's the solution!

## Custom functions

So I guess you're now thinking what kind of functions are in there, and as you
can imagine there's functions for **downloading**, **parsing** and **solving** the daily
challenges!

Here's a list:

   ### Functions:
    
    - help : gives list of available functions
    - clear : clear console history
    - group : used to regroup src in various ways
    - parseday : used to parse a input file which is created by getday to a local variable
    - findsum : 2020 day 1 solve
    - find_increase : day 1 solve 
    - find_arrive : day 2 solve
    - count_commons : day 3 part 1 solve
    - filter_commons : day 3 part 2 solve
    - parse_bingo : parse "src" as bingo boards, use before solve_bingo
    - solve_bingo : day 4 part 1 solve, use after parse_bingo
    - solve_last_bingo : day 4 part 2 solve
    - map_coordinates : day 5 solve
    - evolve_fishes : day 6 solve
    - align_crabs : day 7 solve
    - decode_clock : day 8 solve
    - map_smoke_flows : day 9 solve
    - validate_navigation : day 10 solve
    - light_octopuses : day 11 solve
    

   ### Day shortcuts:
    - 2020 day 1 
    - day 1
    - day 2
    - day 3 1
    - day 3 2
    - day 4 1
    - day 4 2
    - day 5
    - day 6
    - day 7
    - day 8
    - day 9
    - day 10
    - day 11

   ### Bash command:
    - getday <day>: downloads a day's input from adventofcode.com
    - foo : you should't try it
    - rm <path>: removes a file
    - cat <path>: shows content of a text file located into /inputs folder
    
    remember the file path on Windows uses '\', in UNIX with '/'

If instead **you need help with the command usage, try typing the command itself**, the
CLI will provide you with arguments explaination
## Features

### Live output:
The CLI will execute the command you're typing in a sandbox enviroment everytime you press a charachter on your keyboard,
when you press `Enter` the modifications you see wil be executed

### Command history:
To **navigate your command history** use the keys '\`' for moving back and '~' for forward,
at startup history will be populated with enviromental variables

### Autocomplete:
To **use autocomplete** simply type part of the desired command, and then click 'TAB',
click repeatedly to navigate

### Enviromental variables:
As most of the CLIs it uses **enviromental variables**, to set them simply write
<ENV_VAR> = <new value> into the CLI
#### Enviromental variables(Default value):
   - OUT_LEN(150): length of output before being truncated
