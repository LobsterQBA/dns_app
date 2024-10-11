from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def query_authoritative_server(as_ip, as_port, hostname):
    """
    向权威服务器发送DNS查询请求，获取斐波那契服务器的IP地址。
    """
    import socket
    server_address = (as_ip, int(as_port))
    message = f"TYPE=A\nNAME={hostname}\n"
    
    # 创建UDP套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 发送查询请求
        sock.sendto(message.encode(), server_address)
        
        # 接收响应
        data, _ = sock.recvfrom(4096)
        return data.decode()
    finally:
        sock.close()

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    # 解析请求参数
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    # 检查参数是否完整
    if not all([hostname, fs_port, number, as_ip, as_port]):
        return "Missing parameters", 400

    # 向权威服务器查询斐波那契服务器的IP地址
    dns_response = query_authoritative_server(as_ip, as_port, hostname)
    if "VALUE=" not in dns_response:
        return "Fibonacci server not found", 404

    # 从DNS响应中提取斐波那契服务器的IP地址
    fs_ip = dns_response.split("VALUE=")[1].split()[0]

    # 向斐波那契服务器发送请求获取斐波那契数列
    try:
        fibonacci_response = requests.get(f'http://{fs_ip}:{fs_port}/fibonacci?number={number}')
        if fibonacci_response.status_code == 200:
            return fibonacci_response.text, 200
        else:
            return "Error from Fibonacci server", 500
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
