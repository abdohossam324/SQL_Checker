تنزيل الأداة: قم بتنزيل الأداة من [GitHub repository] أو قم باستنساخ المستودع إلى جهازك:

bash
Copy code
git clone https://github.com/your-username/sql-injection-tool.git
تثبيت مكتبة requests: لتثبيت مكتبة requests التي تعتمد عليها الأداة، يمكنك استخدام الأمر التالي:

bash
Copy code
pip install requests
كيفية الاستخدام:
بعد تثبيت المكتبات، يمكنك تشغيل الأداة باستخدام Python.

انتقل إلى المجلد الذي يحتوي على السكربت ثم شغل الأداة باستخدام الأمر التالي:

bash
Copy code
python check_sql_injection.py
إدخال الرابط الذي تريد فحصه: عند تشغيل الأداة، ستُطلب منك إدخال الرابط الذي تريد فحصه. قم بإدخال الرابط الذي يحتوي على معلمات في الاستعلام (مثل ?id=1):

bash
Copy code
Enter the URL to check for SQL injection: http://example.com/page?id=1
نتيجة الفحص: بعد الفحص، ستظهر رسالة توضح ما إذا كان الرابط يحتوي على ثغرة SQL Injection أم لا.

إذا كانت هناك ثغرة، سيتم طباعة:

arduino
Copy code
The URL http://example.com/page?id=1 is vulnerable to SQL injection.
إذا لم تكن هناك ثغرة، سيتم طباعة:

arduino
Copy code
The URL http://example.com/page?id=1 is not vulnerable to SQL injection.
كيف تعمل الأداة:
تقوم الأداة بفحص الرابط عن طريق إضافة بعض payloads الشائعة المستخدمة لاكتشاف ثغرات SQL Injection في المعلمات المختلفة. إذا تم العثور على خطأ في الاستعلام (مثل أخطاء SQL أو رسائل من MySQL)، تعتبر الأداة أن الرابط قد يكون عرضة للثغرة.

ملاحظات:
تأكد من أنك تمتلك إذنًا لفحص الموقع، حيث أن الفحص غير المصرح به قد يكون غير قانوني.
الأداة لا تضمن اكتشاف جميع أنواع SQL Injection. يجب استخدام أدوات أكثر تطورًا لفحص الأمان بشكل أعمق.
إضافة اسم الصانع:
تم تطوير هذه الأداة بواسطة:

Abdelrhman Nada
