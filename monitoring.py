import psutil
import socket

def check_ram():
    # Récupère la mémoire utilisée
    ram = psutil.virtual_memory()
    return {
        "total": ram.total,
        "available": ram.available,
        "percent": ram.percent,
        "used": ram.used,
        "free": ram.free
    }

def check_disk():
    # Récupère l'utilisation du disque pour le disque où est monté '/'
    disk = psutil.disk_usage('/')
    return {
        "total": disk.total,
        "used": disk.used,
        "free": disk.free,
        "percent": disk.percent
    }

def check_cpu():
    # Récupère l'utilisation du CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    return {
        "cpu_percent": cpu_percent
    }

def check_tcp_ports(ports):
    # Vérifie si les ports TCP spécifiés sont ouverts
    port_status = {}
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex(('localhost', port))
            port_status[port] = result == 0
    return port_status

def check_system(tcp_ports):
    # Intègre toutes les vérifications
    return {
        "ram": check_ram(),
        "disk": check_disk(),
        "cpu": check_cpu(),
        "tcp_ports": check_tcp_ports(tcp_ports)
    }
