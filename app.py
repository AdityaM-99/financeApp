from flask import Flask, request, jsonify
import requests
import stocks
import pandas as pd
app = Flask(__name__)
import os
cwd = os.getcwd()
csv_path = os.path.join(cwd,"stocks.xlsx") #cwd+"stocks.xlsx"
@app.route('/get_stock_price', methods=['POST'])
def get_stock_price_endpoint():
    data = request.get_json()
    symbol = data.get('symbol')
    if not symbol:
        return jsonify({'Error': 'No symbol provided'}), 400
    
    stock_data = stocks.get_stock_price(symbol)
    return jsonify(stock_data)


@app.route('/add_symbol', methods=['POST'])
def add_symbol():
    data = request.get_json()
    symbol = data.get('symbol')
    print(symbol)
    if not symbol:
        return jsonify({'Error': 'No symbol provided'}), 400
    
    csv=pd.read_excel(csv_path)
    print('csv::')
    print(csv)
    if symbol in csv['symbol'].values:
        return jsonify({'Error': 'Symbol already exists'}), 400
    
    get_stock_price = stocks.get_stock_price(symbol)
    if 'Error' in get_stock_price:
        return jsonify({'Error': get_stock_price['Error']}), 400
    get_stock_price['symbol'] = symbol
    
    new_row = pd.DataFrame([get_stock_price])
    csv = pd.concat([csv, new_row], ignore_index=True)
    csv.to_excel(csv_path, index=False)
    #csv[len(csv)] = get_stock_price
    #csv.to_csv(csv_path, index=False)
    print(csv)
    return jsonify({'Message': f'Symbol {symbol} added successfully'}), 200

@app.route('/get_all_prices', methods=['GET'])
def get_all_prices():
    try:
        csv = pd.read_excel(csv_path)
        print( jsonify(csv.to_dict(orient='records')))
        return jsonify(csv.to_dict(orient='records')), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
    
@app.route('/update_prices', methods=['GET'])
def update_prices():
    try:
        csv = pd.read_excel(csv_path)
        for index, row in csv.iterrows():
            symbol = row['symbol']
            stock_data = stocks.get_stock_price(symbol)
            if stock_data and 'Error' not in stock_data:
                csv.at[index, 'Current Price'] = stock_data['Current Price']
                csv.at[index, 'Opening Price'] = stock_data['Opening Price']
                csv.at[index, 'Closing Price'] = stock_data['Closing Price']
                csv.at[index, 'High'] = stock_data['High']
                csv.at[index, 'Low'] = stock_data['Low']
        csv.to_excel(csv_path, index=False)
        return jsonify({'Message': 'Prices updated successfully'}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500
    
@app.route('/delete_symbol', methods=['POST'])
def delete_symbol():
    data = request.get_json()
    symbol = data.get('symbol')
    if not symbol:
        return jsonify({'Error': 'No symbol provided'}), 400
    
    csv = pd.read_excel(csv_path)
    if symbol not in csv['symbol'].values:
        return jsonify({'Error': 'Symbol not found'}), 404
    
    csv = csv[csv['symbol'] != symbol]
    csv.to_excel(csv_path, index=False)
    return jsonify({'Message': f'Symbol {symbol} deleted successfully'}), 200

if __name__ == "__main__":
    app.run(debug=True)