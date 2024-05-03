import pprint
def print_chat(dict):
    pprint.pp(dict)

def print_assitant(str):
    print("\033[92m"+str+"\033[0m")

def print_error(str):
    print("\033[93m"+str+"\033[0m")

def print_function_log(str):
    print("\033[94m"+str+"\033[0m")
