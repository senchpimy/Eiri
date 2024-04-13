import req
import functions as F
from chat import Chat

AI = req.AI(mode="ollama")

def addition(x:int, y:int) -> int:
    return x + y

def subtraction(x:int, y:int)->int:
    return x - y

def get_current_time()->str:
    return "Time now"

class Timer:
    def __init__(self)->None:
        self.description = "The first argument must be a string, specifically either 'minutes' or 'hours'. The second argument must be an integer representing the quantity."
        self.examples = [
                {"role": "user", "content": "Given the request 'Set a timer for thirty minutes' and the function 'timer' wich takes 2 arguments with the notation (str, int), which arguments are the correct to fullfill the request"},
                {"role": "assistant", "content": f"minutes,30\n"},
            ]

    def execute(self, time:str, cuantity:int):
        print(f"IT WAS EXECUTED: {cuantity} {time}")
        pass

    def verify(self, time:str, cuantity:int)-> bool:
         if time not in ['minutes', 'hours']:
             return False
         return True

f = F.Functions(AI)
f.add(get_current_time)
f.add(Timer)

chat = Chat(f, AI)

while True:
    print("loop 5")
    p = input("> ")
    chat.evaluate_propmpt(p)
    #chat.require_fuction(p)
