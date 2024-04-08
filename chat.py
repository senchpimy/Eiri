import functions as F
import req

class Chat():
    def __init__(self, f:F.Functions, AI:req.AI, role:str|None = None):
        self.avaible_functions = f.avaible_functions()
        if not role:
            role = f"""
            You are 'Eiri' a virtual assistant that can complete any task, your principal porpuse its to chat with the user, the user may ask you to execute some of the following functions: {" ,".join(self.avaible_functions)}
            Assume that the user know you, what you can do and what every functions does, you will not explin you abilitites unless you are asked to do so, 
            you will NOT give examples of how to use the functions, not you will try to solve them
            the system will tell you when a function was executed and what was its output if id had any

            Dont worry about executing a function your main porpuse its to talk with the user
            """
        self.history = [{"role": "system", "content":role}]
        self.AI = AI
        self.f = f

    def evaluate_propmpt(self,prompt:str):
        self.history.append({"role": "user", "content": prompt})
        if self.require_fuction(prompt):
            result = self.f.evaluate_propmt(prompt) #Get result execute properly
            match result.output:
                case F.EnumResult.ERROR:
                    pass
        res = self.AI.chat_complete(self.history,100)
        print("\033[92m"+res+"\033[0m") # This line messes auto indentation for some reason
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
        response = self.AI.chat_complete(messages,1,mode="instruct")
        result = self.get_truefalse(response)
        while result == None:
            print(response)
            response = self.AI.chat_complete(messages,1,mode="instruct")
            result = self.get_truefalse(response)
        return result

    def require_fuction(self,prompt:str)->bool:
        messages=[
            {"role": "system", "content": f"Given a prompt, answer 'F' for false or 'T' for true if the prompt is a petition to execute any of the this fucntions: {self.avaible_functions} "},
            {"role": "user", "content": "Hi, How are you doing today?"},
            {"role": "assistant", "content": "F\n"},
            {"role": "user", "content": "What time is it"},
            {"role": "assistant", "content": "T\n"},
            {"role": "user", "content": "Set a timer for five minutes"},
            {"role": "assistant", "content": "T\n"},
            {"role": "user", "content": prompt},]
        response = self.AI.chat_complete(messages,1, mode="instruct")
        result = self.get_truefalse(response)
        while result == None:
            print(response)
            response = self.AI.chat_complete(messages,1,mode="instruct")
            result = self.get_truefalse(response)
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

