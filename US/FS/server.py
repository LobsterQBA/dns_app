from flask import Flask, request, jsonify
import json
import socket

app = Flask(__name__)

def register_with_as(hostname, ip, as_ip, as_port):
    """
    向权威服务器注册斐波那契服务器的主机名和IP地址。
    """
    server_address = (as_ip, int(as_port))
    message = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n"
    
    # 创建UDP套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 发送注册请求
        sock.sendto(message.encode(), server_address)
        # 接收响应
        data, _ = sock.recvfrom(4096)
        return data.decode()
    finally:
        sock.close()

@app.route('/register', methods=['PUT'])
def register():
    """
    处理 PUT 请求以注册斐波那契服务器。
    """
    data = request.get_json()
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = data.get('as_port')

    if not all([hostname, ip, as_ip, as_port]):
        return "Missing parameters", 400

    # 向权威服务器注册
    response = register_with_as(hostname, ip, as_ip, as_port)
    return f"Registered with AS: {response}", 201

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    """
    计算并返回指定斐波那契数列的值。
    """
    number = request.args.get('number')

    if not number.isdigit():
        return "Invalid number", 400

    # 计算斐波那契数列
    n = int(number)
    fib_value = calculate_fibonacci(n)

    return jsonify({"Fibonacci": fib_value}), 200

def calculate_fibonacci(n):
    """
    计算斐波那契数列的第 n 项。
    """
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
