# ترجمة صفحات المواعيد للطبيب إلى الفرنسية

## ✅ التحديثات المطبقة

### 🔧 **1. إصلاح عرض العمر في صفحة المرضى:**

#### **إضافة خاصية age في نموذج Patient (`models.py`):**
```python
@property
def age(self):
    """حساب عمر المريض بناءً على تاريخ الميلاد"""
    if self.birth_date:
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
    return None
```

#### **تحسين عرض العمر في template (`doctor/patients.html`):**
```html
<td>
    {% if patient.age %}
        {{ patient.age }} ans
    {% else %}
        <span class="text-muted">Non spécifié</span>
    {% endif %}
</td>
```

### 🌐 **2. ترجمة صفحة appointments (`doctor/appointments.html`):**

#### **حالات المواعيد:**
```html
{% if appointment.status == 'مجدول' or appointment.status == 'Programmé' %}
    <span class="badge bg-primary">Programmé</span>
{% elif appointment.status == 'مكتمل' or appointment.status == 'Terminé' %}
    <span class="badge bg-success">Terminé</span>
{% elif appointment.status == 'ملغي' or appointment.status == 'Annulé' %}
    <span class="badge bg-danger">Annulé</span>
{% elif appointment.status == 'فائت' or appointment.status == 'Manqué' %}
    <span class="badge bg-warning">Manqué</span>
{% endif %}
```

#### **الأزرار والإجراءات:**
- `عرض التفاصيل` → `Voir les détails`
- `عرض الزيارة` → `Voir la visite`
- `تحديد كمكتمل` → `Marquer comme terminé`
- `تحديد كفائت` → `Marquer comme manqué`

#### **الترقيم:**
- `السابق` → `Précédent`
- `التالي` → `Suivant`

#### **الرسائل:**
- `لا توجد مواعيد بحالة` → `Aucun rendez-vous avec le statut`
- `لا توجد مواعيد مجدولة حتى الآن` → `Aucun rendez-vous programmé pour le moment`
- `العودة للوحة التحكم` → `Retour au tableau de bord`

#### **JavaScript:**
```javascript
function updateStatus(appointmentId, newStatus) {
    if (confirm(`Êtes-vous sûr de vouloir changer le statut du rendez-vous à "${newStatus}" ?`)) {
        // Code...
    }
}
```

### 🌐 **3. ترجمة صفحة view_appointment (`doctor/view_appointment.html`):**

#### **العناوين الرئيسية:**
- `تفاصيل الموعد` → `Détails du rendez-vous`
- `معلومات المريض` → `Informations du patient`
- `تفاصيل الموعد` → `Détails du rendez-vous`
- `الزيارة المرتبطة` → `Visite associée`
- `إجراءات الموعد` → `Actions du rendez-vous`

#### **معلومات المريض:**
- `الاسم الكامل` → `Nom complet`
- `رقم الهاتف` → `Numéro de téléphone`
- `تاريخ الميلاد` → `Date de naissance`
- `الجنس` → `Sexe`
- `زمرة الدم` → `Groupe sanguin`
- `العنوان` → `Adresse`
- `ذكر` → `Homme`
- `أنثى` → `Femme`
- `غير محدد` → `Non spécifié`

#### **تفاصيل الموعد:**
- `تاريخ الموعد` → `Date du rendez-vous`
- `وقت الموعد` → `Heure du rendez-vous`
- `حالة الموعد` → `Statut du rendez-vous`
- `تاريخ الإنشاء` → `Date de création`
- `آخر تحديث` → `Dernière mise à jour`
- `ملاحظات الموعد` → `Notes du rendez-vous`

#### **معلومات الزيارة:**
- `تاريخ الزيارة` → `Date de la visite`
- `حالة الزيارة` → `Statut de la visite`
- `سعر الزيارة` → `Prix de la visite`
- `حالة الدفع` → `Statut de paiement`
- `التشخيص` → `Diagnostic`
- `العلاج` → `Traitement`

#### **حالات الزيارة:**
- `مستقر` → `Stable`
- `متابعة` → `Suivi`
- `طارئ` → `Urgence`
- `معلقة` → `En attente`

#### **حالات الدفع:**
```html
{% if appointment.visit.payment_status == 'payé' %}
    <span class="badge bg-success">Payé</span>
{% elif appointment.visit.payment_status == 'non_payé' %}
    <span class="badge bg-danger">Non payé</span>
{% elif appointment.visit.payment_status == 'partiellement_payé' %}
    <span class="badge bg-warning">Partiellement payé</span>
{% endif %}
```

#### **الأزرار والإجراءات:**
- `تحديد كمكتمل` → `Marquer comme terminé`
- `تحديد كفائت` → `Marquer comme manqué`
- `إلغاء الموعد` → `Annuler le rendez-vous`
- `العودة لقائمة المواعيد` → `Retour à la liste des rendez-vous`
- `حذف الموعد` → `Supprimer le rendez-vous`
- `عرض تفاصيل الزيارة كاملة` → `Voir les détails complets de la visite`

#### **الرسائل:**
- `لم يتم تسجيل تشخيص` → `Aucun diagnostic enregistré`
- `لم يتم تسجيل علاج` → `Aucun traitement enregistré`

#### **JavaScript:**
```javascript
function updateStatus(newStatus) {
    if (confirm(`Êtes-vous sûr de vouloir changer le statut du rendez-vous à "${newStatus}" ?`)) {
        // Code...
    }
}
```

#### **تأكيد الحذف:**
```html
onsubmit="return confirm('Êtes-vous sûr de vouloir supprimer ce rendez-vous ?')"
```

### 💰 **4. توحيد العملة:**
- تم تغيير جميع العملات من `ل.س` إلى `DA`

### 🔄 **5. دعم الحالات المختلطة:**
- تم إضافة دعم للحالات العربية والفرنسية معاً
- مثال: `appointment.status == "مجدول" or appointment.status == "Programmé"`

## 🧪 كيفية الاختبار

### **1. اختبار عرض العمر:**
1. اذهب إلى صفحة المرضى للطبيب
2. تأكد من ظهور العمر بـ "ans" للمرضى الذين لديهم تاريخ ميلاد
3. تأكد من ظهور "Non spécifié" للمرضى بدون تاريخ ميلاد

### **2. اختبار صفحة المواعيد:**
1. اذهب إلى صفحة المواعيد للطبيب
2. تأكد من ظهور الحالات بالفرنسية (Programmé, Terminé, Annulé, Manqué)
3. جرب الفلتر والترقيم
4. جرب تحديث حالة موعد

### **3. اختبار صفحة تفاصيل الموعد:**
1. انقر على "Voir les détails" لأي موعد
2. تأكد من ترجمة جميع العناوين والنصوص
3. تأكد من عرض حالة الدفع بالفرنسية
4. جرب أزرار الإجراءات

### **4. اختبار الأزرار:**
1. جرب "Marquer comme terminé"
2. جرب "Marquer comme manqué"
3. جرب "Supprimer le rendez-vous"
4. تأكد من ظهور رسائل التأكيد بالفرنسية

## 🎯 النتائج المتوقعة

### **صفحة المرضى:**
- ✅ عرض العمر بـ "ans" أو "Non spécifié"
- ✅ جميع النصوص مترجمة للفرنسية

### **صفحة المواعيد:**
- ✅ حالات المواعيد بالفرنسية
- ✅ أزرار وتوضيحات مترجمة
- ✅ رسائل التأكيد بالفرنسية
- ✅ الترقيم بالفرنسية

### **صفحة تفاصيل الموعد:**
- ✅ جميع العناوين والحقول مترجمة
- ✅ حالات الزيارة والدفع بالفرنسية
- ✅ أزرار الإجراءات مترجمة
- ✅ رسائل التأكيد بالفرنسية

---

**جاهز للاختبار! 🚀**

الآن صفحات المواعيد للطبيب مترجمة بالكامل إلى الفرنسية مع إصلاح مشكلة عرض العمر.