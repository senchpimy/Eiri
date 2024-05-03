import multiprocessing
import functions as F
import req
import log

manager = multiprocessing.Manager()

def simple_chat(chat, p):
    res = chat.AI.chat_complete(chat.history)
    p["res"] = res

class Chat():
    def __init__(self, f:F.Functions, AI:req.AI, role:str|None = None):
        self.avaible_functions = f.avaible_functions()
        if not role:
            role = f"""
            <s>[INST] <<SYS>>
            You are 'Eiri' a virtual assistant that can complete any task, your principal porpuse its to chat with the user, the user may ask you to execute some of the following functions: {" ,".join(self.avaible_functions)}
The user already know you, knows what you can do and knows what every functions does, you will NOT explain you abilitites and you will NOT give examples or tell the user about what you can do UNLESS you are asked to do so.
you will NOT give examples of how to use the functions, nor you will try to solve them
the system will tell you when a function was executed and what was its output if id had any

Dont make up facts about the functions, you will report what the system tell you about the function

Dont worry about executing a function your main porpuse its to talk with the user, so tal to them with a friendly actitude, try to be funny

<</SYS>>
"""
        self.history = [{"role": "system", "content":role}]
        self.AI = AI
        self.f = f
        self.last_response = manager.dict()


    def evaluate_propmpt(self,prompt:str):
        self.history.append({"role": "user", "content": prompt})
        if self.require_function(prompt):
            result = self.f.evaluate_propmt(prompt)
            match result.o_enum:
                case F.EnumResult.ERROR:
                    self.history.append({"role": "user", "content": f"<s>[INST] <<SYS>>\nThe function throw a exception:{result.report}.\nERROR: {result.error}\nInform the user about this\n<</SYS>>"}) #TODO more handle?
                case F.EnumResult.SUCCES:
                    try:
                        output_str = f" and the function returned {str(result.value)}" if result.value else ""
                    except: #The result doesnt implement __str__()
                        output_str = ""
                    self.history.append({"role": "user", "content": f"<s>[INST] <<SYS>>\nThe function was succesfully executed:{result.report}{output_str}\nInform the user about this\n<</SYS>>"})
        p = multiprocessing.Process(target=simple_chat,args=(self,self.last_response))
        p.start()
        p.join(5)
        if p.is_alive():
            p.terminate()
            print("Tardo Demasiado!!")
            nw_prompt = self.history[-1]["content"]
            self.history[-1]["content"] = nw_prompt+". Please keep it short" # Limiting the ouput
            self.last_response["res"]=  self.AI.chat_complete(self.history,stop="\n")
        res = self.last_response["res"]
        log.print_assitant(res)
        self.history.append({"role": "assistant", "content": res})

    def confirm_request(self):
        pass

    def require_function(self,prompt:str)->bool:
        system = f"""You are analyzing messages of a user one at a time, the user is having a conversation your task is to read the message and decide if he wants to execute a function, 
given a message, answer 'F' for false or 'T' for true if the prompt is a petition to execute any of the this fucntions: {self.avaible_functions} """
        exa_messages=[
            {"role": "system", "content": system},

            {"role": "user", "content": "Hi, How are you doing today?"},
            {"role": "assistant", "content": "F\n"},

            {"role": "user", "content": "What time is it"},
            {"role": "assistant", "content": "T\n"},

            {"role": "user", "content": "Set a timer for five minutes"},
            {"role": "assistant", "content": "T\n"},

            #{"role": "user", "content": "Can you remind me to buy milk?"},
            #{"role": "assistant", "content": "T\n"},
            #
            #{"role": "user", "content": "Calculate the square root of 144."},
            #{"role": "assistant", "content": "T\n"},
            #
            #{"role": "user", "content": "Play some music."},
            #{"role": "assistant", "content": "T\n"},
            #
            #{"role": "user", "content": "Tell me a joke."},
            #{"role": "assistant", "content": "T\n"},
            #
            #{"role": "user", "content": "Open the weather app."},
            #{"role": "assistant", "content": "F\n"},
            #
            #{"role": "user", "content": "Can you search for restaurants nearby?"},
            #{"role": "assistant", "content": "T\n"},
            #
            #{"role": "user", "content": "Turn off the lights in the living room."},
            #{"role": "assistant", "content": "T\n"},
            #
            #{"role": "user", "content": "What's the capital of France?"},
            #{"role": "assistant", "content": "F\n"},

            {"role": "user", "content": prompt},]
        response = self.AI.chat_complete(exa_messages,1)
        result = self.get_truefalse(response)
        tries = 5
        while result == None:
            response = self.AI.chat_complete(exa_messages,1)
            result = self.get_truefalse(response)
            tries-=1
            if not tries:
                print("MAX TRIES REACHED")
                return False
        return result

    def get_truefalse(self,text:str)->bool|None:
        response = ''.join(text.split())
        print(response)
        val = None
        if response == 'T':
            val = True
        elif response == 'F':
            val = False
        return val

    def print_log(self):
        log.print_chat(self.history)

