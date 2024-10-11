import socket
import json

# 权威服务器的 IP 和端口
AS_IP = '0.0.0.0'
AS_PORT = 53533

# 存储DNS记录的文件
DNS_RECORD_FILE = 'dns_records.json'

def load_dns_records():
    """加载DNS记录文件"""
    try:
        with open(DNS_RECORD_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_dns_record(hostname, ip):
    """保存新的DNS记录"""
    records = load_dns_records()
    records[hostname] = ip
    with open(DNS_RECORD_FILE, 'w') as file:
        json.dump(records, file)

def handle_registration(data):
    """处理斐波那契服务器的注册请求"""
    lines = data.splitlines()
    record_type = lines[0].split('=')[1]
    hostname = lines[1].split('=')[1]
    ip_address = lines[2].split('=')[1]
    ttl = lines[3].split('=')[1]

    if record_type == 'A':
        save_dns_record(hostname, ip_address)
        return f"Registered {hostname} -> {ip_address}"

def handle_dns_query(data):
    """处理DNS查询请求"""
    lines = data.splitlines()
    record_type = lines[0].split('=')[1]
    hostname = lines[1].split('=')[1]

    if record_type == 'A':
        records = load_dns_records()
        if hostname in records:
            ip_address = records[hostname]
            return f"TYPE=A\nNAME={hostname}\nVALUE={ip_address}\nTTL=10"
        else:
            return "Record not found"

def start_authoritative_server():
    """启动权威服务器"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((AS_IP, AS_PORT))

    print(f"Authoritative server is running on {AS_IP}:{AS_PORT}...")

    while True:
        data, address = sock.recvfrom(4096)
        data = data.decode()

        if 'VALUE=' in data:  # 判断是注册请求
            response = handle_registration(data)
        else:  # 否则是DNS查询请求
            response = handle_dns_query(data)

        sock.sendto(response.encode(), address)

if __name__ == '__main__':
    start_authoritative_server()
