import stripe
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Замени на свой Secret Key из Stripe Dashboard
stripe.api_key = "sk_test_51TDj6YHbcDp4NhtiIgDk3fpSFTALcPB3ObpKLjUChWVzcA7Vh7l7WknWEaYQK90TRtZPzXYyrCEnyaFVGzBfC5ck00ZZmqoo2A"

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        data = request.get_json()
        customer_name = data.get('customerName', 'Пользователь')
        
        # Создаём сессию оплаты
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'rub',
                    'product_data': {
                        'name': 'SafeWalk Premium',
                        'description': 'Доступ к расширенным функциям безопасности',
                    },
                    'unit_amount': 29900,  # 299 рублей в копейках
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:8080/profile.html?success=true',
            cancel_url='http://localhost:8080/profile.html?canceled=true',
            customer_email=f"{customer_name.lower().replace(' ', '.')}@example.com",
        )
        
        return jsonify({'url': checkout_session.url})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(port=5000)