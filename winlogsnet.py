import tkinter as tk
from tkinter import scrolledtext
import psutil
import socket

def get_ips():
    result = "[ IPs da Máquina ]\n"
    ips = psutil.net_if_addrs()
    for iface, addr_list in ips.items():
        for addr in addr_list:
            if addr.family == socket.AF_INET:
                result += f"Interface: {iface}\tIP: {addr.address}\n"
    return result + "\n"

def get_processos():
    result = "[ Processos/Aplicativos Rodando ]\n"
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            result += f"PID: {proc.info['pid']}\tNome: {proc.info['name']}\tUsuário: {proc.info['username']}\n"
        except Exception:
            continue
    return result + "\n"

def get_servicos():
    result = "[ Serviços Windows Ativos ]\n"
    try:
        for serv in psutil.win_service_iter():
            s = serv.as_dict()
            if s['status'] == 'running':
                result += f"Serviço: {s['name']} - {s['display_name']}\n"
    except Exception:
        result += "Serviços só disponíveis no Windows\n"
    return result + "\n"

def get_conexoes():
    result = "[ Conexões de Rede ]\n"
    for conn in psutil.net_connections(kind='inet'):
        laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
        raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
        pid = conn.pid
        status = conn.status
        try:
            app_name = psutil.Process(pid).name() if pid else "N/A"
        except Exception:
            app_name = "Erro/Desconhecido"
        result += f"Local: {laddr}\tRemoto: {raddr}\tStatus: {status}\tPID: {pid}\tApp: {app_name}\n"
    return result + "\n"

def atualizar():
    saida = ""
    saida += get_ips()
    saida += get_processos()
    saida += get_servicos()
    saida += get_conexoes()
    
    
    filtro = entry_filtro.get().strip()
    if filtro:
        linhas = saida.split('\n')
        saida_filtrada = "\n".join([linha for linha in linhas if filtro.lower() in linha.lower()])
        saida = saida_filtrada
    
    txt_saida.config(state='normal')
    txt_saida.delete('1.0', tk.END)
    txt_saida.insert(tk.END, saida)
    txt_saida.config(state='disabled')
    root.after(3000, atualizar)  # Atualiza a cada 3 segundos

root = tk.Tk()
root.title("Monitor Completo de Sistema - Filtro")
root.geometry("1000x740")
root.configure(bg="#23272f")

label_title = tk.Label(root, text="Monitor de Sistema com Busca/Filtro", bg="#23272f", fg="#fafafa", font=("Arial", 16, "bold"))
label_title.pack(pady=10)

frame_filtro = tk.Frame(root, bg="#23272f")
frame_filtro.pack()

tk.Label(frame_filtro, text="Filtrar por palavra/porta/nome/IP:", bg="#23272f", fg="#fafafa", font=("Arial", 12)).pack(side=tk.LEFT, padx=4)
entry_filtro = tk.Entry(frame_filtro, width=30, font=("Consolas", 12))
entry_filtro.pack(side=tk.LEFT, padx=4)

txt_saida = scrolledtext.ScrolledText(root, width=120, height=38, font=("Consolas", 10), bg="#212223", fg="#fff")
txt_saida.pack(padx=10, pady=10)
txt_saida.config(state='disabled')

atualizar()
root.mainloop()
