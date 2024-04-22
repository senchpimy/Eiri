class AI:
    def __init__(self,mode="request",base_url="http://127.0.0.1:5000/v1", model=None):
        assert (mode in ["request", "ollama"])
        self.lib = None
        self.model=model
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

    def chat_complete_requests(self,messages:list[dict[str,str]],  max_tokens = None,stop=None, model=None, mode:str|None = None )->str:
        assert (mode in ["chat", "instruct"])
        url  = self.base_url+"/chat/completions"
        use_model = self.model if model == None else model
        data = {
            "model":use_model,
            "mode": mode,
            "character": "Example",
            "user_bio": "",
            "user_name": "",
            "messages": messages,
        }
        if max_tokens:
            data["max_tokens"]=max_tokens
        if stop:
            data["stop"] = stop
        response = self.lib.post(url, headers=self.headers, json=data, verify=False)
        assistant_message = response.json()['choices'][0]['message']['content']
        return assistant_message

    def chat_complete_ollama(self,messages:list[dict[str,str]],  max_tokens = None,stop=None, model=None, mode:str|None = None )->str:
        url  = self.base_url+"/chat/completions"
        use_model = self.model if model == None else model
        data = {
            "model":use_model,
            "character": "Example",
            "user_bio": "",
            "user_name": "",
            "messages": messages,
            "stream":False
        }
        if max_tokens:
            data["max_tokens"]=max_tokens
        if stop:
            data["stop"]=stop
        #response = ollama.chat(model=model, messages=messages, max_tokens=max_tokens)
        response = self.lib.post(url, headers=self.headers, json=data, verify=False)
        assistant_message = response.json()['choices'][0]['message']['content']
        #assistant_message = response.json()
        return assistant_message







