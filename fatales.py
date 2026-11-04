from flask import Flask, render_template, request, redirect, url_for, session
import webbrowser
from threading import Timer

app = Flask(__name__)
app.secret_key = 'secret_key_fatales'

@app.route('/')
def home():
    total_items = sum(item['quantity'] for item in session.get('panier', []))
    return render_template('fatales.html', total_items=total_items)

@app.route('/ajouter', methods=['POST'])
def ajouter():
    product_name = request.form.get('product_name')
    product_price = float(request.form.get('product_price'))
    quantity = int(request.form.get('quantity'))

    panier = session.get('panier', [])
    for item in panier:
        if item['name'] == product_name:
            item['quantity'] += quantity
            break
    else:
        panier.append({'name': product_name, 'price': product_price, 'quantity': quantity})

    session['panier'] = panier
    return redirect(url_for('voir_panier'))

@app.route('/panier')
def voir_panier():
    panier = session.get('panier', [])
    total = sum(item['price'] * item['quantity'] for item in panier)
    return render_template('panier.html', panier=panier, total=total)

@app.route('/valider', methods=['POST'])
def valider():
    session.pop('panier', None)
    return render_template('merci.html')

if __name__ == '__main__':
    Timer(1, lambda: webbrowser.open('http://127.0.0.1:5000')).start()
    app.run(debug=True, port=5000)