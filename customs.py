import typer
import requests
import os

app = typer.Typer()
@app.command()
def getday(day:int):
    cookief = open("cookie.txt", 'r+')
    token = cookief.read()
    if not token:
        print("Session cookie not found, to set it simply write it into the just created cookie.txt")
        exit()
    if not os.path.exists('inputs'):
        os.makedirs('inputs')
    with requests.Session() as s:
        s.cookies.set("session", token, domain=".adventofcode.com")
        data = s.get(f"https://adventofcode.com/2021/day/{day}/input")
        with open(f"inputs/{day}.txt", 'w') as fd:
            fd.write(data.text)
        print(f"{day}.txt created")

@app.command()
def foo():
    print("yeah that's useless lol")

if __name__ == "__main__":
    app()