import inspect
from enum import Enum
import req

class EnumResult(Enum):
    SUCCES=0 # The function executed correctly
    ERROR=1 # The function failed
    SYNTAX_ERROR=2 # Wrong format for the function

class FunctionResult:
    def __init__(self,value, o_enum:EnumResult) -> None:
        self.value = value
        self.o_enum = o_enum


class Functions:
    def __init__(self,AI:req.AI,end = None) -> None:
        self.fn= {}
        self.end = "\n" if end is None else end
        self.logger_arr = []
        self.AI = AI

    def count_arguments(self,func):
        return inspect.signature(func).parameters
    
    def avaible_functions(self)->list[str]:
        return list(self.fn.keys())

    def add(self, cl):
        self.fn[cl.__name__.lower()] = cl #To lower???

    def execute_function(self, func, name,args=None)->FunctionResult:
        if args:
            try:
                out = func(*args)
            except:
                out = EnumResult.ERROR
        else:
            try:
                out = func()
            except:
                out = EnumResult.ERROR
        if out == EnumResult.ERROR:
            return FunctionResult(None,out)

        output = f" with result {out}" if out else ""
        self.log(f"Executed fuction {name}{output}")
        return FunctionResult(out,EnumResult.SUCCES)

    def get_posibble_function(self, prompt:str)->str:
        #Verify that the function exists
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
            response = self.AI.chat_complete(messages,10)
            answer_first:str = response.lower().replace(" ","").replace(" ","") #To lower???
            result = answer_first.split("\n")[0]
        return result

    def logger(self,log):
        self.logger_arr = log


    def log(self,result:str):
        #print('\033[94m'+result+'\033[0m')
        log = {"role": "user", "content": result},
        self.logger_arr.append(log)

    def evaluate_propmt(self,prompt:str)->FunctionResult:
        result = self.get_posibble_function(prompt)
        func = self.fn[result]
        messages=[
                    {"role": "system", "content": "Given a request to execute a function with a specified signature, provide the correct arguments to fulfill the request"},
                    {"role": "user", "content": "Given the request 'What is the value of the sum of the numbers 5 then 7' and the function 'addition' wich takes 2 arguments with the notation (int, int), which arguments are the correct to fullfill the request"},
                    {"role": "assistant", "content": f"5,7{self.end}"},
                    {"role": "user", "content": "Given the request 'How much is 14 minus 9' and the function 'substraction' wich takes 2 arguments with the notation (int, int), which arguments are the correct to fullfill the request"},
                    {"role": "assistant", "content": f"14,9{self.end}"},
                    #{"role": "user", "content": full_prompt},
                ]

        if isinstance(func,type):
            instance = func()
            insp = self.count_arguments(instance.execute) #Verify that such function exists
            if len(insp)==0:
                return self.execute_function(instance.execute,result)

            types = [nota.annotation for nota in insp.values()]
            ## TODO add the description
            optional = ""
            if hasattr(instance, "description"):
                optional= f" with the description '{instance.description}'"
            full_prompt=f"Given the request '{prompt}' and the function '{result}'{optional} wich takes {len(insp)} arguments with the notation ({', '.join([nota.__name__ for nota in types])}), which arguments are the correct to fullfill the request"
            print("########################")
            print(full_prompt)
            print("########################")
            messages.append({"role": "user", "content": full_prompt})
            if hasattr(instance, "examples"):
                messages=messages[:-2] + instance.examples + messages[-2:]
            while True:
                print("loop 2")
                response = self.AI.chat_complete(messages,20)
                answer :str = response.lower().replace(" ","").replace(" ","").split("\n")[0]
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
                    return self.execute_function(instance.execute,result,args_correct)
        else:
            insp = self.count_arguments(func)
            if len(insp)==0:
                return self.execute_function(func,result)
            types = [nota.annotation for nota in insp.values()]
            full_prompt=f"Given the request '{prompt}' and the function '{result}' wich takes {len(insp)} arguments with the notation ({', '.join([nota.__name__ for nota in types])}), which arguments are the correct to fullfill the request"
            print("########################")
            print(full_prompt)
            print("########################")
            messages.append({"role": "user", "content": full_prompt})
            while True:
                response = self.AI.chat_complete(messages,20)
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
                    #return func(*args_correct)
                    return self.execute_function(func,result,args_correct)
