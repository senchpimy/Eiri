import inspect
import openai
from openai import OpenAI

client = OpenAI(api_key="",base_url="http://127.0.0.1:5000/v1")

add_propmpt = "What is the value of the sum of the numbers 3 then 4"
subtract_propmpt = "What is the value of the substraction of the numbers 3 then 4"
time_propmpt = "What time is it"
timer_propmpt = "Set a timer for five minutes"

def addition(x:int, y:int) -> int:
    return x + y

def subtraction(x:int, y:int)->int:
    return x - y

def time()->str:
    return "Time now"

class Timer:
    def __init__(self)->None:
        self.description = "The first argument must be a string, specifically either 'minutes' or 'hours'. The second argument must be an integer representing the quantity."
        self.examples = [
                {"role": "user", "content": "Given the request 'Set a timer for thirty minutes' and the function 'timer' wich takes 2 arguments with the notation (str, int), which arguments are the correct to fullfill the request"},
                {"role": "assistant", "content": f"minutes,30\n"},
            ]

    def execute(self, time:str, cuantity:int):
        print(f"IT WAS EXECUTED {time}, sakjajk {cuantity}")
        pass

    def verify(self, time:str, cuantity:int)-> bool:
        if time not in ['minutes', 'hours']:
            return False
        return True

class Functions:
    def __init__(self,end = None) -> None:
        self.fn= {}
        self.end = "\n" if end is None else end
        # TODO: The 'openai.api_base' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(base_url="http://127.0.0.1:5000/v1")'
        # openai.api_base = "http://127.0.0.1:5000/v1"

    def count_arguments(self,func):
        return inspect.signature(func).parameters

    def add(self, cl):
        self.fn[cl.__name__.lower()] = cl #To lower???

    def evaluate_propmt(self,prompt:str):
        full_prompt=f"Given the following list of functions, please select the one that is best suited to fullfill the request '{prompt}':  {', '.join(self.fn.keys())} "
        result = ""
        while result not in self.fn:
            response = client.chat.completions.create(model="llama",
            messages=[
                {"role": "system", "content": "You are an assistant that can only answer ONE word"},
                {"role": "user", "content": "Given the following list of functions, please select the one that is best suited to fullfill the request 'How much is 5 plus 7': addition, subtraction, time"},
                {"role": "assistant", "content": f"addition{self.end}"},
                {"role": "user", "content": "Given the following list of functions, please select the one that is best suited to fullfill the request 'How much is 14 minus 9': addition, subtraction, time"},
                {"role": "assistant", "content": f"subtraction{self.end}"},
                {"role": "user", "content": "Given the following list of functions, please select the one that is best suited to fullfill the request 'What time it is?': addition, subtraction, time"},
                {"role": "assistant", "content": f"time{self.end}"},
                {"role": "user", "content": full_prompt},
            ],
            max_tokens=8,
            )
            print(response)
            print(self.fn)
            answer_first:str = response.choices[0].message.content.lower().replace(" ","") #To lower???
            result = answer_first.split("\n")[0]
            print(result)
        
        func = self.fn[result]

        if isinstance(func,type):
            instance = func()
            insp = self.count_arguments(instance.execute)
            if len(insp)>0:
                types = [nota.annotation for nota in insp.values()]
                ## TODO add the description
                optional = ""
                if hasattr(instance, "description"):
                    optional= f" with the description '{instance.description}'"
                full_prompt=f"Given the request '{prompt}' and the function '{result}'{optional} wich takes {len(insp)} arguments with the notation ({', '.join([nota.__name__ for nota in types])}), which arguments are the correct to fullfill the request"
                print("########################")
                print(full_prompt)
                print("########################")
                messages = [
                            {"role": "system", "content": "Given a request to execute a function with a specified signature, provide the correct arguments to fulfill the request"},
                            {"role": "user", "content": "Given the request 'What is the value of the sum of the numbers 5 then 7' and the function 'addition' wich takes 2 arguments with the notation (int, int), which arguments are the correct to fullfill the request"},
                            {"role": "assistant", "content": f"5,7{self.end}"},
                            {"role": "user", "content": "Given the request 'How much is 14 minus 9' and the function 'substraction' wich takes 2 arguments with the notation (int, int), which arguments are the correct to fullfill the request"},
                            {"role": "assistant", "content": f"14,9{self.end}"},
                            {"role": "user", "content": full_prompt},
                        ]
                if hasattr(instance, "examples"):
                    messages=messages[:-2] + instance.examples + messages[-2:]
                while True:
                    response = client.chat.completions.create(model="llama",
                    messages=messages,
                    max_tokens=20)
                    answer :str = response.choices[0].message.content.lower().replace(" ","").split("\n")[0]
                    print("ANSWER:"+answer)
                    args = answer.split(",")
                    args_correct = []
                    cont = False
                    if len(insp) == len(args) == len(types):
                        for index,arg in enumerate(args):
                            try:
                                args_correct.append(types[index](arg)) ## Some parsing could be useful
                            except:
                                cont = True
                        if cont: continue
                        if hasattr(instance, "verify"):
                            if not instance.verify(*args_correct): continue
                        print("###TERMINATE####")
                        return instance.execute(*args_correct)
            else:
                return instance.execute()
        else:
            insp = self.count_arguments(func)
            if len(insp)>0:
                types = [nota.annotation for nota in insp.values()]
                full_prompt=f"Given the request '{prompt}' and the function '{result}' wich takes {len(insp)} arguments with the notation ({', '.join([nota.__name__ for nota in types])}), which arguments are the correct to fullfill the request"
                print("########################")
                print(full_prompt)
                print("########################")
                while True:
                    response = client.chat.completions.create(model="llama",
                    messages=[
                        {"role": "system", "content": "Given a request to execute a function with a specified signature, provide the correct arguments to fulfill the request"},
                        {"role": "user", "content": "Given the request 'What is the value of the sum of the numbers 5 then 7' and the function 'addition' wich takes 2 arguments with the notation (int, int), which arguments are the correct to fullfill the request"},
                        {"role": "assistant", "content": f"5,7{self.end}"},
                        {"role": "user", "content": "Given the request 'How much is 14 minus 9' and the function 'substraction' wich takes 2 arguments with the notation (int, int), which arguments are the correct to fullfill the request"},
                        {"role": "assistant", "content": f"14,9{self.end}"},
                        {"role": "user", "content": full_prompt},
                    ],
                    max_tokens=20)
                    answer :str = response.choices[0].message.content.lower().replace(" ","").split("\n")[0]
                    print("ANSWER:"+answer)
                    args = answer.split(",")
                    args_correct = []
                    cont = False
                    if len(insp) == len(args) == len(types):
                        for index,arg in enumerate(args):
                            try:
                                args_correct.append(types[index](arg)) ## Some parsing could be useful
                            except:
                                cont = True
                        if cont: continue
                        return func(*args_correct)
            else: return func()

f = Functions()
f.add(addition)
f.add(subtraction)
f.add(time)
f.add(Timer)

print(f.evaluate_propmt(add_propmpt))
print(f.evaluate_propmt(subtract_propmpt))
print(f.evaluate_propmt(time_propmpt))
print(f.evaluate_propmt(timer_propmpt))
