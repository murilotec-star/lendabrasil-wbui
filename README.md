import requests
import re
from mcrcon import MCRcon
import time

# ============================
# CONFIGURAÇÕES
# ============================

ASA_API_URL = "https://seu-asa-bot/api/players"   # URL da API do ASA-Bot
ASA_API_TOKEN = "SEU_TOKEN_AQUI"

RCON_IP = "127.0.0.1"
RCON_PORT = 27020
RCON_PASSWORD = "SENHA_RCON"

DISCORD_LINK = "https://discord.gg/seu-servidor"

# Regex para detectar nomes humanos
REGEX_NOME_HUMANO = r"^[A-Z][a-z]{2,15}$"

# Mensagem enviada ao jogador
MENSAGEM = (
    "[AVISO] Seu nome não segue as regras do servidor. "
    f"Abra um ticket no Discord para solicitar alteração: {DISCORD_LINK}"
)

# Kick automático? (True/False)
KICKAR = False


# ============================
# FUNÇÕES
# ============================

def obter_jogadores():
    headers = {"Authorization": f"Bearer {ASA_API_TOKEN}"}
    try:
        r = requests.get(ASA_API_URL, headers=headers, timeout=10)
        return r.json()
    except:
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


# ============================
# LOOP PRINCIPAL
# ============================

print("Monitor de nomes iniciado...")

while True:
    jogadores = obter_jogadores()

    for j in jogadores:
        nome = j.get("character", "")
        steamid = j.get("player_id", "")

        if nome_e_humano(nome):
            print(f"[DETECTADO] {nome} ({steamid})")
            enviar_rcon(steamid, MENSAGEM)

    time.sleep(30)  # verifica a cada 30 segundos
