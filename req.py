import requests

class AI:
    def __init__(self,base_url="http://127.0.0.1:5000/v1"):
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json"
        }
        pass
    def chat_complete(self,messages:list[dict[str,str]], max_tokens:int,model:str="Llama", mode:str|None = None )->str:
        if mode == None or mode not in ["chat","instruct"]:
            mode = "instruct"
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
        response = requests.post(url, headers=self.headers, json=data, verify=False)
        assistant_message = response.json()['choices'][0]['message']['content']
        return assistant_message







