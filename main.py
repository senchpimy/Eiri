import inspect
import openai

add_propmpt = "What is the value of the sum of the numbers 3 then 4"
subtract_propmpt = "What is the value of the substraction of the numbers 3 then 4"
time_propmpt = "What time is it"

def addition(x:int, y:int) -> int:
    return x + y

def subtraction(x:int, y:int)->int:
    return x - y

def time()->str:
    return "Time now"

class Functions:
    def __init__(self,end = None) -> None:
        self.fn= {}
        self.end = "\n" if end is None else end
        openai.api_base = "http://127.0.0.1:5000/v1"
        openai.api_key = ""

    def count_arguments(self,func):
        return inspect.signature(func).parameters

    def add(self, cl):
        self.fn[cl.__name__] = cl

    def evaluate_propmt(self,prompt:str):
        full_prompt=f"Given the following list of functions, please select the one that is best suited to fullfill the request '{prompt}':  {', '.join(self.fn.keys())} "
        result = ""
        while result not in self.fn:
            response = openai.ChatCompletion.create(
                model="llama",
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
                max_tokens=8
            )
            print(response)
            answer_first:str = response['choices'][0]['message']['content'].lower().replace(" ","")
            result = answer_first.split("\n")[0]
        
        func = self.fn[result]
        insp = self.count_arguments(func)
        if len(insp)>0:
            types = [nota.annotation for nota in insp.values()]
            full_prompt=f"Given the request '{prompt}' and the function '{result}' wich takes {len(insp)} arguments with the notation ({', '.join([nota.__name__ for nota in types])}), which arguments are the correct to fullfill the request"
            print("########################")
            print(full_prompt)
            print("########################")
            while True:
                response = openai.ChatCompletion.create(
                    model="llama",
                    messages=[
                        {"role": "system", "content": "Given a request to execute a function with a specified signature, provide the correct arguments to fulfill the request"},
                        {"role": "user", "content": "Given the request 'What is the value of the sum of the numbers 5 then 7' and the function 'addition' wich takes 2 arguments with the notation (int, int), which arguments are the correct to fullfill the request"},
                        {"role": "assistant", "content": f"5,7{self.end}"},
                        {"role": "user", "content": "Given the request 'How much is 14 minus 9' and the function 'substraction' wich takes 2 arguments with the notation (int, int), which arguments are the correct to fullfill the request"},
                        {"role": "assistant", "content": f"14,9{self.end}"},
                        {"role": "user", "content": full_prompt},
                    ],
                    max_tokens=20  
                )
                answer :str = response['choices'][0]['message']['content'].lower().replace(" ","").split("\n")[0]
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

print(f.evaluate_propmt(add_propmpt))
print(f.evaluate_propmt(subtract_propmpt))
print(f.evaluate_propmt(time_propmpt))
