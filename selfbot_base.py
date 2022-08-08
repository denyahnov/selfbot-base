import os
import re
import json
import discord
from requests import get, post
from discord.ext.commands import Bot
from urllib.request import Request, urlopen

client = Bot(command_prefix='!',self_bot=True,description='''SelfBot Base'''); line=''
ascii_title = '    _____      _  ________       _    ______ \n   /  ___|    | |/ _| ___ \     | |   | ___ \               \n   \ `--.  ___| | |_| |_/ / ___ | |_  | |_/ / __ _ ___  ___ \n    `--. \/ _ \ |  _| ___ \/ _ \| __| | ___ \/ _` / __|/ _ \ \n   /\__/ /  __/ | | | |_/ / (_) | |_  | |_/ / (_| \__ \  __/\n   \____/ \___|_|_| \____/ \___/ \__| \____/ \__,_|___/\___|'
for i in range(80): line+='='


def check_token(token):
    response = get('https://discordapp.com/api/users/@me', headers={"Authorization": token})
    return response.text if response.status_code != 401 else False

def find_tokens(path):
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens

def main():
    tkns=[]
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')

    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        tokens = find_tokens(path)

        if len(tokens) > 0:
            for token in tokens:
                tkns.append(token)

    return tkns

@client.event
async def on_ready():
    print("Logged into {}".format(client.user) + '\n' + line)

if __name__ == '__main__':
    os.system('cls')
    os.system('color 0B')
    print(ascii_title + '\n' + line)
    tokens = main()

    if len(tokens) < 1: raise Exception

    tkn_real=''

    print('[+] Searching {} Possibilities'.format(len(tokens)))

    for tkn in tokens:
        data = check_token(tkn)
        if data:
            tkn_real = tkn
            break

    if tkn_real != '': 
        for d in data.split(','):
            if 'username' in d:
                d = d.replace('"username": ','')
                username = d.replace('"','')[1:]
            elif 'discriminator' in d:
                d = d.replace('"discriminator": ','')
                tag = d.replace('"','')[1:]

        print('[+] Found Account {}'.format(username+'#'+tag))

        input(f'{line}\n[!] WARNING: This application is bannable, are you sure you want to continue?\n[?] Press ENTER to Continue\n{line}')

        try:
            client.run(tkn_real)
        except:
            print("[!] ERROR: Could not connect to Discord client! Check internet connection")
            exit(0)
    else: 
        print('[!] ERROR: Could not find account on device')
        exit(0)