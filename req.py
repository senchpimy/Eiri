import ollama

class AI:
    def __init__(self,mode="request",base_url="http://127.0.0.1:5000/v1"):
        assert (mode in ["request", "ollama"])
        self.lib = None
        match mode:
            case "request":
                import requests as lib
                self.lib = lib
                self.chat_complete=self.chat_complete_requests
                self.base_url = base_url
                self.headers = {
                    "Content-Type": "application/json"
                }
            case "ollama":
                import requests as lib
                self.lib = lib
                self.chat_complete=self.chat_complete_ollama
                self.base_url = "http://127.0.0.1:11434/v1"
                self.headers = {
                    "Content-Type": "application/json"
                }

    def chat_complete_requests(self,messages:list[dict[str,str]], max_tokens:int,model:str="Llama", mode:str|None = None )->str:
        assert (mode in ["chat", "instruct"])
        url  = self.base_url+"/chat/completions"
        data = {
            "model":model,
            "mode": mode,
            "character": "Example",
            "user_bio": "",
            "user_name": "",
            "messages": messages,
            "max_tokens":max_tokens
        }
        response = self.lib.post(url, headers=self.headers, json=data, verify=False)
        assistant_message = response.json()['choices'][0]['message']['content']
        return assistant_message

    def chat_complete_ollama(self,messages:list[dict[str,str]], max_tokens:int,model:str="mistral", mode:str|None = None )->str:
        url  = self.base_url+"/chat/completions"
        data = {
            "model":model,
            "character": "Example",
            "user_bio": "",
            "user_name": "",
            "messages": messages,
            "max_tokens":max_tokens,
            "stream":False
        }
        #response = ollama.chat(model=model, messages=messages, max_tokens=max_tokens)
        response = self.lib.post(url, headers=self.headers, json=data, verify=False)
        assistant_message = response.json()['choices'][0]['message']['content']
        #assistant_message = response.json()
        return assistant_message







