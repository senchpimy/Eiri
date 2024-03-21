import inspect
import req

AI = req.AI()

add_propmpt = "What is the value of the sum of the numbers 3 then 4"
subtract_propmpt = "What is the value of the substraction of the numbers 3 then 4"
time_propmpt = "What time is it"
timer_propmpt = "Set a timer for five minutes"

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

    def count_arguments(self,func):
        return inspect.signature(func).parameters
    
    def avaible_functions(self)->list[str]:
        return list(self.fn.keys())

    def add(self, cl):
        self.fn[cl.__name__.lower()] = cl #To lower???

    def evaluate_propmt(self,prompt:str):
        full_prompt=f"Given the following list of functions, please select the one that is best suited to fullfill the request '{prompt}':  {', '.join(self.fn.keys())} "
        result = ""
        while result not in self.fn:
            messages=[
                {"role": "system", "content": "You are an assistant that can only answer ONE word"},
                {"role": "user", "content": "Given the following list of functions, please select the one that is best suited to fullfill the request 'How much is 5 plus 7': addition, subtraction, time"},
                {"role": "assistant", "content": f"addition{self.end}"},
                {"role": "user", "content": "Given the following list of functions, please select the one that is best suited to fullfill the request 'How much is 14 minus 9': addition, subtraction, time"},
                {"role": "assistant", "content": f"subtraction{self.end}"},
                {"role": "user", "content": "Given the following list of functions, please select the one that is best suited to fullfill the request 'What time it is?': addition, subtraction, time"},
                {"role": "assistant", "content": f"time{self.end}"},
                {"role": "user", "content": full_prompt}
                ]
            response = AI.chat_complete(messages,8)
            print(response)
            print(self.fn)
            answer_first:str = response.lower().replace(" ","") #To lower???
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
                    response = AI.chat_complete(messages,20)
                    answer :str = response.lower().replace(" ","").split("\n")[0]
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
                    messages=[
                        {"role": "system", "content": "Given a request to execute a function with a specified signature, provide the correct arguments to fulfill the request"},
                        {"role": "user", "content": "Given the request 'What is the value of the sum of the numbers 5 then 7' and the function 'addition' wich takes 2 arguments with the notation (int, int), which arguments are the correct to fullfill the request"},
                        {"role": "assistant", "content": f"5,7{self.end}"},
                        {"role": "user", "content": "Given the request 'How much is 14 minus 9' and the function 'substraction' wich takes 2 arguments with the notation (int, int), which arguments are the correct to fullfill the request"},
                        {"role": "assistant", "content": f"14,9{self.end}"},
                        {"role": "user", "content": full_prompt},
                    ]
                    response = AI.chat_complete(messages,20)
                    answer :str = response.lower().replace(" ","").split("\n")[0]
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
#f.add(addition)
#f.add(subtraction)
f.add(get_current_time)
f.add(Timer)

class Chat():
    def __init__(self, f:Functions):
        self.avaible_functions = f.avaible_functions()
        self.history = [{"role": "system", "content":"You are a virtual assistant, you have no body, you are living inside a computer that is able to execute some functions"}]
        print(self.avaible_functions)
    def evaluate_propmpt(self,prompt:str):
        self.history.append({"role": "user", "content": prompt})
        if self.require_fuction(prompt):
            f.evaluate_propmt(prompt)
            #TODO How can I continue
        res = AI.chat_complete(self.history,100)
        print('\033[92m'+res+'\033[0m')
        self.history.append({"role": "assistant", "content": res})
    def confirm_selection(self, prompt:str)->bool:
        messages=[
            {"role": "system", "content": f"Answer 'F' If you dont agree or 'T' if you do  with the prompt, and justify your answer"},
            {"role": "user", "content": "Do you agree that no action should be done to fullfill the request 'Hi, How are you doing today?'"},
            {"role": "assistant", "content": "T\n"},
            {"role": "user", "content": "Do you agree that no action should be done to fullfill the request 'Set a timer for five minutes'"},
            {"role": "assistant", "content": "F\n"},
            {"role": "user", "content": prompt},
        ]
        print(messages)
        response = AI.chat_complete(messages,60)
        while response not in ["F","T"]:
            print(response)
            response = AI.chat_complete(messages,1)
        res =  True if response == "T" else False
        return res

    def require_fuction(self,prompt:str)->bool:
        messages=[
            {"role": "system", "content": f"Given a prompt, answer 'F' for false or 'T' for true if the prompt is a petition to execute any of the this fucntions: {self.avaible_functions} "},
            {"role": "user", "content": "Hi, How are you doing today?"},
            {"role": "assistant", "content": "F\n"},
            {"role": "user", "content": "What time is it"},
            {"role": "assistant", "content": "T\n"},
            {"role": "user", "content": "Set a timer for five minutes"},
            {"role": "assistant", "content": "T\n"},
            {"role": "user", "content": prompt},
        ]
        response = AI.chat_complete(messages,1, mode="instruct")
        print(response)
        while response not in ["F","T"]:
            print(response)
            response = AI.chat_complete(messages,1,mode="instruct")
        res =  True if response == "T" else False
        return res
        #verb = f"an execution of any of the functions {self.avaible_functions}" if res else "no action"
        #print("CONFIRM")
        #print(prompt)
        #return self.confirm_selection(f"Do you agree that {verb} should be done to fulfill the request '{prompt}'")

chat = Chat(f)

#print(f.evaluate_propmt(add_propmpt))
#print(f.evaluate_propmt(subtract_propmpt))
#print(f.evaluate_propmt(time_propmpt))
#print(f.evaluate_propmt(timer_propmpt))
#print(f.evaluate_propmt("Hola como estas?"))
while True:
    p = input("> ")
    chat.evaluate_propmpt(p)
    #chat.require_fuction(p)
