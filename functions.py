import inspect
from enum import Enum
import req

def toInt(value)-> int|None:
    try:
        return int(value)
    except ValueError:
        try:
            return int(value.strip("'\""))
        except ValueError:
            return None

def toFloat(value)-> float|None:
    try:
        return float(value)
    except ValueError:
        try:
            return float(value.strip("'\""))
        except ValueError:
            return None

def toString(value:str)-> str|None:
    if value.startswith(('"',"'")) and value.endswith(('"',"'")):
        value = value[1:-1]
    return value

def cut_string(text):
    for i, char in enumerate(text):
        if char in [".",",","-"]:
            return text[:i]
    return text

types_covert={
        int:toInt,
        str:toString,
        float:toFloat,
        }

class EnumResult(Enum):
    SUCCES=0 # The function executed correctly
    ERROR=1 # The function failed
    SYNTAX_ERROR=2 # Wrong format for the function

class FunctionResult:
    def __init__(self,value, o_enum:EnumResult) -> None:
        self.value = value
        self.o_enum = o_enum

class Functions:
    def __init__(self,AI:req.AI, max_tries=7) -> None:
        self.fn= {}
        self.logger_arr = []
        self.AI = AI
        self.max_tries = max_tries

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
        #   Verify that the function exists
        #   Return Error if its not found
        #   Give feedback
        full_prompt=f"Given the following list of functions, please select the one that is best suited to fullfill the request '{prompt}':  {', '.join(self.fn.keys())} "
        print(full_prompt)
        result = ""
        num_tries = 0
        messages=[ #Añadir ejemplos de cada funcion
            {"role": "system", "content": "You are an assistant that can only answer ONE word"},
            {"role": "user", "content": "Given the following list of functions, please select the one that is best suited to fullfill the request 'How much is 5 plus 7': addition, subtraction, time,timer"},
            {"role": "assistant", "content": f"addition\n"},
            {"role": "user", "content": "Given the following list of functions, please select the one that is best suited to fullfill the request 'How much is 14 minus 9': addition, subtraction, time, timer"},
            {"role": "assistant", "content": f"subtraction\n"},
            {"role": "user", "content": "Given the following list of functions, please select the one that is best suited to fullfill the request 'What time it is?': addition, subtraction, time, timer"},
            {"role": "assistant", "content": f"time\n"},
            {"role": "user", "content": full_prompt}
        ]
        while result not in self.fn and num_tries<self.max_tries:
            response = self.AI.chat_complete(messages,20)
            print(response)
            answer_first:str = response.lower().replace(" ","").replace(" ","") #To lower???
            preresult = answer_first.split("\n")[0]
            result = cut_string(preresult)
            num_tries+=1
        if num_tries==self.max_tries:
            #TODO return a error
            pass
        return result

    def logger(self,log):
        self.logger_arr = log

    def log(self,result:str):
        print('\033[94m'+result+'\033[0m')
        log = {"role": "user", "content": result},
        self.logger_arr.append(log)

    def evaluate_propmt(self,prompt:str)->FunctionResult:
        result = self.get_posibble_function(prompt)
        func = self.fn[result]
        messages=[
                    {"role": "system", "content": "Given a request to execute a function with a specified signature, provide the correct arguments to fulfill the request"},
                    {"role": "user", "content": "Given the request 'What is the value of the sum of the numbers 5 then 7' and the function 'addition' wich takes 2 arguments with the notation (int, int), which arguments are the correct to fullfill the request"},
                    {"role": "assistant", "content": f"5,7"},
                    {"role": "user", "content": "Given the request 'How much is 14 minus 9' and the function 'substraction' wich takes 2 arguments with the notation (int, int), which arguments are the correct to fullfill the request"},
                    {"role": "assistant", "content": f"14,9"},
                   # {"role": "user", "content": full_prompt},
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
                response = self.AI.chat_complete(messages,50)
                #answer :str = response.lower().replace(" ","").replace(" ","").split("\n")[0]
                answer :str = response.lower()#.split("\n")
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
            types = [types_covert[nota.annotation] for nota in insp.values()]
            full_prompt=f"Given the request '{prompt}' and the function '{result}' wich takes {len(insp)} arguments with the notation ({', '.join([nota.__name__ for nota in types])}), which arguments are the correct to fullfill the request"
            #print("########################")
            #print(full_prompt)
            #print("########################")
            messages.append({"role": "user", "content": full_prompt})
            while True:
                print("loop 3")
                response = self.AI.chat_complete(messages,20)
                answer :str = response.lower().replace(" ","").split("\n")[0]
                print("ANSWER:"+answer)
                args = answer.split(",")
                args_correct = []
                cont = False
                if len(insp) == len(args) == len(types):
                    for index,arg in enumerate(args):
                        try:
                            args_correct.append(types[index](arg))
                        except:
                            cont = True
                            break
                    if cont: continue
                    #return func(*args_correct)
                    return self.execute_function(func,result,args_correct)
