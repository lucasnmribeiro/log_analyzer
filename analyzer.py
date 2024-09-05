import pandas as pd
import smtplib
from email.mime.text import MIMEText
import os

def carregar_logs(caminho_arquivo):
    try:
        logs = pd.read_csv(caminho_arquivo)
        return logs
    except Exception as e:
        print(f"Erro ao carregar arquivo: {e}")
        return None

def detectar_tentativas_falhas(logs):
    tentativas_falhas = logs[logs['EventID'] == 4625]
    return tentativas_falhas

def detectar_acessos_suspeitos(logs):
    acessos_suspeitos = logs.groupby('IPAddress').filter(lambda x: len(x) > 5)
    return acessos_suspeitos

def enviar_alerta(email_destino, mensagem):
    try:
        remetente = 'seuemail@gmail.com'
        senha = 'sua_senha'

        msg = MIMEText(mensagem)
        msg['Subject'] = 'Alerta de Segurança - Log Analyzer'
        msg['From'] = remetente
        msg['To'] = email_destino

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as servidor:
            servidor.login(remetente, senha)
            servidor.sendmail(remetente, email_destino, msg.as_string())
            print("Alerta enviado!")
    except Exception as e:
        print(f"Erro ao enviar alerta: {e}")

def alerta_sonoro_windows():
    duration = 1000
    freq = 440
    os.system('powershell [console]::beep({}, {})'.format(freq, duration))

if __name__ == "__main__":
    caminho = input("Insira o caminho do arquivo de logs (CSV): ")
    logs = carregar_logs(caminho)
    if logs is not None:
        tentativas_falhas = detectar_tentativas_falhas(logs)
        acessos_suspeitos = detectar_acessos_suspeitos(logs)
        
        if not tentativas_falhas.empty:
            mensagem = f"Tentativas de login falhas detectadas: {len(tentativas_falhas)} eventos."
            enviar_alerta('email@examplo.com', mensagem)
            alerta_sonoro_windows()
        
        if not acessos_suspeitos.empty:
            mensagem = f"Acessos suspeitos detectados de {len(acessos_suspeitos['IPAddress'].unique())} IPs diferentes."
            enviar_alerta('email@examplo.com', mensagem)
            alerta_sonoro_windows()