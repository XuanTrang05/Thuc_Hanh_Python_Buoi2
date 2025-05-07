from flask import Flask, render_template
import requests
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# API URLs
GOLD_API_URL = 'https://www.goldapi.io/api/XAU/USD'  # Thay thế metals-api bằng goldapi.io
WEATHER_API_URL = 'https://api.open-meteo.com/v1/forecast?latitude=21.0285&longitude=105.8542&current_weather=true'
CURRENCY_API_URL = 'https://v6.exchangerate-api.com/v6/d8193d6ede36b4b8b827265b/latest/USD'

# Hàm lấy dữ liệu giá vàng
def get_gold_price():
    try:
        headers = {
            'x-access-token': 'YOUR_GOLDAPI_KEY'  # Thay YOUR_GOLDAPI_KEY nếu có
        }
        response = requests.get(GOLD_API_URL, headers=headers).json()
        if 'price' in response:
            return response['price']  # Giá vàng theo USD/ounce
        else:
            return None
    except Exception as e:
        print(f"Error fetching gold price: {e}")
        return None  # Giả lập dữ liệu nếu API không hoạt động

# Tạo biểu đồ giá vàng
def create_gold_chart():
    years = [2019, 2020, 2021, 2022, 2023]
    gold_prices = [1500, 1700, 1800, 1900, 2000]  # Giả lập dữ liệu giá vàng

    plt.figure(figsize=(8, 5))
    plt.plot(years, gold_prices, marker='o', color='gold')
    plt.title('Biểu đồ giá vàng theo năm')
    plt.xlabel('Năm')
    plt.ylabel('Giá vàng (USD/ounce)')
    plt.grid(True)

    # Lưu biểu đồ vào thư mục static
    chart_path = os.path.join('static', 'gold_chart.png')
    plt.savefig(chart_path)
    plt.close()

@app.route('/')
def index():
    # Lấy dữ liệu từ API
    gold_price = get_gold_price()
    weather_data = requests.get(WEATHER_API_URL).json()
    currency_data = requests.get(CURRENCY_API_URL).json()

    # Tạo biểu đồ giá vàng
    create_gold_chart()

    # Kiểm tra và chuẩn bị dữ liệu
    context = {
        'gold_price': gold_price if gold_price else 2300.50,  # Giả lập nếu API thất bại
        'weather_temp': weather_data.get('current', {}).get('temperature', 25),  # Giá trị mặc định 25°C
        'weather_code': weather_data.get('current', {}).get('weathercode', 0),  # Giá trị mặc định 0
        'usd_to_vnd': currency_data.get('conversion_rates', {}).get('VND', 25000)  # Lấy tỷ giá thực tế
    }

    return render_template('index.html', **context)

if __name__ == '__main__':
    app.run(debug=True)