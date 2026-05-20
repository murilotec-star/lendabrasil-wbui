import os
import requests
import re
from mcrcon import MCRcon
import time

ASA_API_URL = os.getenv("ASA_API_URL")
ASA_API_TOKEN = os.getenv("ASA_API_TOKEN")

RCON_IP = os.getenv("RCON_IP")
RCON_PORT = int(os.getenv("RCON_PORT"))
RCON_PASSWORD = os.getenv("RCON_PASSWORD")

DISCORD_LINK = os.getenv("DISCORD_LINK")

REGEX_NOME_HUMANO = r"^[A-Z][a-z]{2,15}$"

MENSAGEM = (
    "[AVISO] Seu nome não segue as regras do servidor. "
    f"Abra um ticket no Discord para solicitar alteração: {DISCORD_LINK}"
)

KICKAR = False

def obter_jogadores():
    headers = {"Authorization": f"Bearer {ASA_API_TOKEN}"}
    try:
        r = requests.get(ASA_API_URL, headers=headers, timeout=10)
        return r.json()
    except Exception as e:
        print("Erro ao obter jogadores:", e)
        return []

def enviar_rcon(steamid, mensagem):
    try:
        with MCRcon(RCON_IP, RCON_PASSWORD, port=RCON_PORT) as mcr:
            mcr.command(f'ServerChatToPlayer {steamid} "{mensagem}"')
            if KICKAR:
                mcr.command(f'KickPlayer {steamid} "Nome inválido. Abra ticket no Discord."')
    except Exception as e:
        print("Erro ao enviar RCON:", e)

def nome_e_humano(nome):
    return re.match(REGEX_NOME_HUMANO, nome) is not None

print("Monitor de nomes iniciado...")

while True:
    jogadores = obter_jogadores()

    for j in jogadores:
        nome = j.get("character", "")
        steamid = j.get("player_id", "")

        if nome_e_humano(nome):
            print(f"[DETECTADO] {nome} ({steamid})")
            enviar_rcon(steamid, MENSAGEM)

    time.sleep(30)
