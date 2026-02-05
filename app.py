from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_socketio import SocketIO
import hashlib, random, datetime, networkx as nx, matplotlib.pyplot as plt
import os

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# ----------------------------
# QKD Simulation
# ----------------------------
class QuantumKeyDistribution:
    def __init__(self):
        self.shared_key = ""

    def simulate_bb84(self):
        bits = [random.choice(['0', '1']) for _ in range(16)]
        self.shared_key = ''.join(bits)
        return self.shared_key

qkd = QuantumKeyDistribution()
quantum_shared_key = qkd.simulate_bb84()

# ----------------------------
# Blockchain Classes
# ----------------------------
class Transaction:
    def __init__(self, sender_id, receiver_id, message, shared_key):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.message = message
        self.shared_key = shared_key
        self.message_hash = hashlib.sha256(message.encode()).hexdigest()
        self.signature = hashlib.sha256(
            (self.message_hash + shared_key).encode()
        ).hexdigest()
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class Blockchain:
    def __init__(self):
        self.chain = []

    def add_transaction(self, tx):
        self.chain.append(tx)
        self.visualize()

    def visualize(self, filename="blockchain_graph.png"):
        if not self.chain:
            return

        G = nx.DiGraph()
        for i, block in enumerate(self.chain):
            node = f"Block {i+1}\n{block.timestamp}"
            G.add_node(node)
            if i > 0:
                prev = f"Block {i}\n{self.chain[i-1].timestamp}"
                G.add_edge(prev, node)

        plt.figure(figsize=(8, 4))
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_size=2500)
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()

blockchain = Blockchain()
messages = []

# ----------------------------
# Routes
# ----------------------------

@app.route("/")
def home():
    return jsonify({"status": "Quantum Blockchain Backend Running"})

@app.route("/messages", methods=["GET"])
def get_messages():
    return jsonify(messages)

@app.route("/send", methods=["POST"])
def send_message():
    data = request.json
    message_text = data.get("message", "")

    tx = Transaction(1, 2, message_text, quantum_shared_key)
    blockchain.add_transaction(tx)

    record = {
        "sender": "Node 1",
        "receiver": "Node 2",
        "message": message_text,
        "timestamp": tx.timestamp
    }

    messages.append(record)
    return jsonify({"status": "success"})

@app.route("/blockchain/image")
def get_image():
    path = "blockchain_graph.png"
    if os.path.exists(path):
        return send_file(path, mimetype="image/png")
    return jsonify({"error": "No visualization yet"}), 404

# ----------------------------
# Run Server
# ----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
