import req
import functions as F
from chat import Chat

AI = req.AI(mode="ollama", model="llama3")

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

class Add_Calendar_Event:
    def __init__(self):
        self.description = "The first argument must be a string representing the title, the second argument must be a string representing the date, and the third argument must be a string representing the description."
        self.examples = [
            {
                "role": "user",
                "content": "Could you please add an event titled 'Conference Call' on 2024-05-03 at 10:00 AM with description 'Discuss quarterly goals'?",
                "response": "Conference Call,2024-05-03,Discuss quarterly goals\n"
            },
            {
                "role": "user",
                "content": "I need to schedule a meeting titled 'Team Sync' for tomorrow with description 'Review project timelines'.",
                "response": "Team Sync,2024-05-02,Review project timelines\n"
            },
            {
                "role": "user",
                "content": "Add an event called 'Lunch with Clients' on 2024-05-05 at 12:30 PM to discuss the new product launch.",
                "response": "Lunch with Clients,2024-05-05,Discuss the new product launch\n"
            }
        ]

    def execute(self, title: str, date: str, description: str):
        print(f"Event '{title}' added on {date} with description: {description}")

    def verify(self, title: str, date: str, description: str) -> bool:
        if not all([title, date, description]):
            return False
        return True

f = F.Functions(AI)
f.add(get_current_time)
f.add(Timer)
f.add(Add_Calendar_Event)

chat = Chat(f, AI)

while True:
    p = input("> ")
    if p == r"\i":
        chat.print_log()
        continue
    chat.evaluate_propmpt(p)
    #chat.require_fuction(p)
