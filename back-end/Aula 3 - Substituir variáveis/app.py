# Importar bibliotecas necessárias  
from flask import Flask, request, jsonify  
from werkzeug.serving import make_server  
import threading  
import requests  
import time  

# Definindo a aplicação Flask  
app = Flask(__name__)  

# Endpoint para somar dois números  
@app.route('/soma', methods=["POST"])  
def soma():  
    dados = request.get_json()  # Obter os dados JSON da requisição  
    numero1 = dados.get("numero1", 0)  
    numero2 = dados.get("numero2", 0)  
    resultado = numero1 + numero2  
    return jsonify({"resultado": resultado})  # Retornar o resultado em formato JSON  

# Classe para rodar o servidor Flask em uma thread separada  
class ThreadedServer(threading.Thread):  
    def __init__(self, app):  
        threading.Thread.__init__(self)  
        self.srv = make_server('127.0.0.1', 5000, app)  
        self.ctx = app.app_context()  
        self.ctx.push()  

    def run(self):  
        print("Servidor Flask iniciado...")  
        self.srv.serve_forever()  

    def shutdown(self):  
        self.srv.shutdown()  

# Iniciar o servidor Flask em uma thread separada  
servidor = ThreadedServer(app)  
servidor.start()  

# Aguardar um pouco para garantir que o servidor esteja rodando  
time.sleep(2)  

# Enviar uma requisição de teste para o endpoint `/soma`  
dados = {"numero1": 0, "numero2": 9}  
resposta = requests.post("http://127.0.0.1:5000/soma", json=dados)  

# Exibir o resultado  
if resposta.status_code == 200:  
    print("Resultado da soma:", resposta.json()["resultado"])  
else:  
    print("Erro na requisição:", resposta.status_code)  

# Encerrar o servidor no final  
servidor.shutdown()