import psutil
import socket

def check_ram():
    ram = psutil.virtual_memory()
    ram_info = {
        "total": ram.total,
        "available": ram.available,
        "percent": ram.percent,
        "used": ram.used,
        "free": ram.free
    }
    print(f"RAM Info: {ram_info}")
    return ram_info

def check_disk():
    disk = psutil.disk_usage('/')
    disk_info = {
        "total": disk.total,
        "used": disk.used,
        "free": disk.free,
        "percent": disk.percent
    }
    print(f"Disk Info: {disk_info}")
    return disk_info

def check_cpu():
    cpu_percent = psutil.cpu_percent(interval=1)
    print(f"CPU Usage: {cpu_percent}%")
    return {"cpu_percent": cpu_percent}

def check_tcp_ports(ports):
    port_status = {}
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex(('localhost', port))
            port_status[port] = result == 0
            print(f"Port {port}: {'Open' if result == 0 else 'Closed'}")
    return port_status

def check_system(tcp_ports):
    print("Starting system checks...")
    system_info = {
        "ram": check_ram(),
        "disk": check_disk(),
        "cpu": check_cpu(),
        "tcp_ports": check_tcp_ports(tcp_ports)
    }
    print("System checks completed.")
    return system_info
