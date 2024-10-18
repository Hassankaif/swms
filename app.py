from flask import Flask, request, jsonify, render_template
from web3 import Web3
import json
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from hybrid_model import apply_hybrid_model
from visualization import create_visualizations

app = Flask(__name__)

# Connect to Ethereum network (replace with your own node URL)
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR-PROJECT-ID'))

# Load ABI and contract address
with open('WaterConservationContract.json') as f:
    contract_json = json.load(f)
contract_abi = contract_json['abi']
contract_address = 'YOUR_CONTRACT_ADDRESS'

# Create contract instance
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Load and preprocess data
df = pd.read_csv('water_consumption_data.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Apply hybrid model
hybrid_results = apply_hybrid_model(df)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/forecast', methods=['GET'])
def get_forecast():
    floor = int(request.args.get('floor'))
    unit = int(request.args.get('unit'))
    
    if (floor, unit) in hybrid_results:
        result = hybrid_results[(floor, unit)]
        return jsonify({
            'forecast': result['forecast'].tolist(),
            'rmse': result['rmse'],
            'top_models': result['top_models']
        })
    else:
        return jsonify({'error': 'No forecast available for this unit'}), 404

@app.route('/visualizations')
def visualizations():
    images = create_visualizations(df, hybrid_results)
    return render_template('visualizations.html', images=images)

@app.route('/report_issue', methods=['POST'])
def report_issue():
    data = request.json
    floor = data['floor']
    unit = data['unit']
    description = data['description']
    user_address = data['user_address']

    # Create transaction
    transaction = contract.functions.reportIssue(floor, unit, description).buildTransaction({
        'from': user_address,
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.get_transaction_count(user_address),
    })

    # Sign and send transaction (in a real app, this would be done client-side)
    private_key = 'USER_PRIVATE_KEY'  # This should be securely managed and not stored in the code
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # Wait for transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    if tx_receipt['status'] == 1:
        return jsonify({'message': 'Issue reported successfully', 'transaction_hash': tx_hash.hex()}), 200
    else:
        return jsonify({'message': 'Failed to report issue'}), 400

@app.route('/get_token_balance', methods=['GET'])
def get_token_balance():
    user_address = request.args.get('address')
    balance = contract.functions.balanceOf(user_address).call()
    return jsonify({'balance': balance}), 200

if __name__ == '__main__':
    app.run(debug=True)