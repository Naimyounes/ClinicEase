# نظام التذاكر مع الأولوية - ClinicEase

## 📋 نظرة عامة

تم تطوير نظام تذاكر متقدم يدعم الأولوية للمرضى الذين لديهم مواعيد مجدولة. النظام يعطي أولوية للمرضى الذين يحضرون في وقت موعدهم أو بعده، مع تمييز خاص برقم التذكرة + حرف R.

## 🎯 الميزات الرئيسية

### 1. نظام التذاكر المزدوج
- **تذاكر عادية**: للمرضى بدون مواعيد (رقم فقط: 1, 2, 3...)
- **تذاكر أولوية**: للمرضى مع مواعيد (رقم + R: 1R, 2R, 3R...)

### 2. حساب الأولوية التلقائي
- يتم فحص وجود موعد للمريض في نفس اليوم
- إذا كان الوقت الحالي >= وقت الموعد → أولوية تلقائية
- التذكرة تحصل على حرف R ومعاملة خاصة

### 3. حساب مدة الانتظار الذكي
- **التذاكر العادية**: من وقت إنشاء التذكرة
- **تذاكر الأولوية**: من وقت الموعد المجدول (ليس من وقت إنشاء التذكرة)

### 4. ترتيب قائمة الانتظار
- الأولوية أولاً (تذاكر R قبل التذاكر العادية)
- ثم الترتيب حسب الرقم تصاعدياً

## 🔧 التطبيق التقني

### تحديثات قاعدة البيانات

#### نموذج Ticket المحدث:
```python
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="waiting")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # حقول نظام الأولوية الجديدة
    ticket_type = db.Column(db.String(20), nullable=False, default="regular")  # regular, reservation
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointment.id"), nullable=True)
    priority = db.Column(db.Integer, nullable=False, default=0)  # 0 = عادي، 1 = أولوية
    
    @property
    def display_number(self):
        return f"{self.number}R" if self.ticket_type == "reservation" else str(self.number)
```

### منطق إنشاء التذكرة

```python
def create_waiting_ticket(patient_id):
    # التحقق من وجود موعد اليوم
    today_appointment = Appointment.query.filter(
        Appointment.patient_id == patient_id,
        db.func.date(Appointment.appointment_date) == today,
        Appointment.status == "مجدول"
    ).first()
    
    # تحديد نوع التذكرة
    ticket_type = "regular"
    priority = 0
    
    if today_appointment:
        appointment_time = today_appointment.appointment_date.time()
        current_time = datetime.now().time()
        
        # إذا حضر في وقت الموعد أو بعده
        if current_time >= appointment_time:
            ticket_type = "reservation"
            priority = 1
            appointment_id = today_appointment.id
```

### ترتيب قائمة الانتظار

```python
waiting_tickets = Ticket.query.filter(
    db.func.date(Ticket.created_at) == today,
    Ticket.status == "waiting"
).order_by(
    Ticket.priority.desc(),  # الأولوية أولاً
    Ticket.number.asc()      # ثم الرقم تصاعدياً
).all()
```

## 🎨 واجهة المستخدم

### مؤشرات بصرية للأولوية

#### في قائمة الانتظار:
- **تذاكر الأولوية**: خلفية صفراء فاتحة
- **رقم التذكرة**: badge أصفر للأولوية، أزرق للعادي
- **أيقونة نجمة**: بجانب اسم المريض للأولوية
- **نوع التذكرة**: عمود منفصل يوضح "أولوية" أو "عادي"

#### في لوحة التحكم:
- **إحصائيات محدثة**: عدد التذاكر مع عدد الأولوية
- **المريض الحالي**: عرض رقم التذكرة مع R إذا كانت أولوية
- **بطاقة قائمة الانتظار**: رابط سريع مع عداد

### حساب مدة الانتظار المحسن

```html
{% if ticket.ticket_type == 'reservation' and ticket.appointment %}
    {% set appointment_time = ticket.appointment.appointment_date %}
    {% set current_time = get_current_datetime() %}
    {% if current_time >= appointment_time %}
        {% set waiting_time = (current_time - appointment_time).total_seconds() / 60 %}
    {% else %}
        {% set waiting_time = 0 %}
    {% endif %}
    <small class="text-muted">منذ وقت الموعد</small>
{% else %}
    {% set waiting_time = (get_current_datetime() - ticket.created_at).total_seconds() / 60 %}
{% endif %}
```

## 📊 سيناريوهات الاستخدام

### السيناريو 1: مريض بدون موعد
1. المريض يصل للعيادة
2. السكرتيرة تنشئ تذكرة عادية
3. يحصل على رقم تسلسلي (مثل: 5)
4. مدة الانتظار تحسب من وقت إنشاء التذكرة

### السيناريو 2: مريض مع موعد - وصل مبكراً
1. المريض لديه موعد الساعة 3:00 PM
2. يصل الساعة 2:30 PM
3. ينشئ تذكرة عادية (6) لأن الوقت لم يحن بعد
4. مدة الانتظار من وقت إنشاء التذكرة

### السيناريو 3: مريض مع موعد - وصل في الوقت أو متأخراً
1. المريض لديه موعد الساعة 3:00 PM
2. يصل الساعة 3:15 PM
3. ينشئ تذكرة أولوية (7R)
4. يحصل على أولوية في القائمة
5. مدة الانتظار تحسب من وقت الموعد (3:00 PM)

## 🔄 تدفق العمل

### إنشاء التذكرة:
1. **اختيار المريض** من قائمة المرضى
2. **فحص تلقائي** لوجود موعد اليوم
3. **تحديد نوع التذكرة** حسب الوقت
4. **إنشاء التذكرة** مع الأولوية المناسبة
5. **إضافة للقائمة** مع الترتيب الصحيح

### استدعاء المرضى:
1. **عرض القائمة** مرتبة حسب الأولوية
2. **استدعاء التالي** (أولوية أولاً)
3. **تحديث الحالة** للتذكرة المستدعاة
4. **إشعار بصري** برقم التذكرة ونوعها

## 📈 الفوائد

### للمرضى:
- **احترام المواعيد**: من لديه موعد لا ينتظر طويلاً
- **شفافية**: رقم التذكرة يوضح نوع الأولوية
- **عدالة**: نظام واضح ومفهوم للجميع

### للعيادة:
- **تنظيم أفضل**: إدارة فعالة لقائمة الانتظار
- **رضا المرضى**: تقليل شكاوى الانتظار
- **كفاءة**: استغلال أمثل لوقت الطبيب

### للسكرتيرة:
- **سهولة الإدارة**: واجهة واضحة ومباشرة
- **معلومات شاملة**: إحصائيات وتفاصيل كاملة
- **مرونة**: إمكانية التحكم في القائمة

## 🎯 الميزات المستقبلية

### تحسينات مقترحة:
1. **إشعارات SMS**: تنبيه المرضى قبل موعدهم
2. **حجز أونلاين**: تذاكر أولوية من الموقع
3. **تقارير تفصيلية**: إحصائيات الانتظار والأولوية
4. **تكامل مع التقويم**: ربط أعمق مع نظام المواعيد

## 🔧 الصيانة والدعم

### ملفات مهمة:
- `clinic_app/models.py`: نماذج قاعدة البيانات
- `clinic_app/secretary/routes.py`: منطق إنشاء التذاكر
- `clinic_app/templates/secretary/waiting_queue.html`: واجهة قائمة الانتظار
- `update_ticket_model.py`: سكريبت تحديث قاعدة البيانات

### نصائح الصيانة:
1. **نسخ احتياطية منتظمة** لقاعدة البيانات
2. **مراقبة الأداء** خاصة مع زيادة عدد التذاكر
3. **تحديث دوري** للواجهات والميزات
4. **تدريب المستخدمين** على النظام الجديد

---

**تاريخ التطوير**: 30 يوليو 2025  
**الإصدار**: 2.0  
**المطور**: فريق ClinicEase  
**الحالة**: مكتمل ومختبر ✅