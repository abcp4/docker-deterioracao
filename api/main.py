from fastapi import FastAPI

app = FastAPI()


def factorial(number):
    if number == 0:
        return 1
    else:
        return number * factorial(number - 1)


@app.get("/factorial")
async def root(number: int):
    """This is a endpoint to find the factorial of an integer"""
    return {"answer": factorial(number)}
