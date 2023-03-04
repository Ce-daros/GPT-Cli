# import
import openai, json

# consts
ORG_KEY = "organization key here"
API_KEY = "api key here"


# functions
def pushConv(role, content):
    conversation.append({"role": role, "content": content})


def getContent(comp):
    return comp["choices"][0]["message"]["content"]


def getRole(comp):
    return comp["choices"][0]["message"]["role"]


def read_status(fname):
    file = open(fname, mode="r", encoding="utf-8")
    status_json = json.loads(file.read())
    file.close()
    return status_json


def write_status(status, fname):
    file = open(fname, mode="w", encoding="utf-8")
    file.write(json.dumps(status, ensure_ascii=False))
    file.close()


# role
role_definition = "role definition here"
env_definition = "env definition here"

# init
openai.organization = ORG_KEY
openai.api_key = API_KEY
print(f"\n\033[92mUse 'help' for help\033[0m")
conversation = [
    {"role": "system", "content": role_definition},
    {"role": "system", "content": env_definition},
]
Text_Err="\033[91m"
Text_Wrn="\033[35;1m"
Text_Cmd="\033[93m"
Text_GPT="\033[34;1m"
Text_ENDL="\033[0m"

# main
while True:
    print(f"\033[0mGPT> ", end="")
    inp = input()
    print("    ",end="")
    if inp[:4] == "help":
        print(f"\033[92m命令列表\n    load  save  reset  quit  help\033[0m")
    elif inp[:4] == "save":
        try:
            write_status(conversation, inp.split(" ")[1])
        except:
            print(Text_Err+f"保存至{inp.split(' ')[1]}失败。"+Text_ENDL)
        else:
            print(Text_Cmd+f"已成功保存至{inp.split(' ')[1]}。"+Text_ENDL)
    elif inp[:4] == "load":
        print(Text_Wrn+f"确定要覆盖当前对话吗？(y/n) "+Text_ENDL,end="")
        if input().lower() == "y":
            try:
                conversation = read_status(inp.split(" ")[1])
            except:
                print(Text_Err+f"读取{inp.split(' ')[1]}失败。"+Text_ENDL)
            else:
                print(Text_Cmd+f"已成功读取{inp.split(' ')[1]}中的对话数据。"+Text_ENDL)
    elif inp[:4] == "quit":
        print(Text_Wrn+f"确定要退出吗？(y/n) "+Text_ENDL,end="")
        if input().lower() == "y":
            exit()
    elif inp[:5] == "reset":
        print(Text_Wrn+f"确定要重置对话吗？(y/n) "+Text_ENDL,end="")
        if input().lower() == "y":
            conversation = [
                {"role": "system", "content": role_definition},
                {"role": "system", "content": env_definition},
            ]

    elif inp == "":
        continue
    else:
        pushConv("user", inp)
        
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=conversation
        )
        if completion['usage']['total_tokens']>=3700:
            del conversation[0]
        pushConv(getRole(completion), getContent(completion))

        print(Text_GPT+f"{getContent(completion)}"+Text_ENDL+f"\033[36m({completion['usage']['total_tokens']})\033[0m")
