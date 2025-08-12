// تحسين التفاعل مع كروت الداشبورد

document.addEventListener('DOMContentLoaded', function() {
    // إضافة تأثيرات الحركة للكروت
    const dashboardCards = document.querySelectorAll('.dashboard-card');
    
    dashboardCards.forEach(card => {
        // إضافة تأثير الدخول
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        // تأخير ظهور الكروت بشكل متتالي
        const delay = Array.from(dashboardCards).indexOf(card) * 100;
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, delay);
        
        // إضافة تأثير النقر للكروت القابلة للنقر
        if (card.classList.contains('clickable-card')) {
            card.addEventListener('click', function(e) {
                // تأثير الضغط
                this.style.transform = 'translateY(-3px) scale(0.98)';
                
                setTimeout(() => {
                    this.style.transform = 'translateY(-5px) scale(1)';
                }, 150);
            });
        }
        
        // إضافة تأثير التمرير
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // تحديث الأرقام بتأثير العد
    const numberElements = document.querySelectorAll('.dashboard-card h2, .dashboard-card h4');
    
    numberElements.forEach(element => {
        const finalNumber = parseInt(element.textContent) || 0;
        if (finalNumber > 0) {
            animateNumber(element, 0, finalNumber, 1000);
        }
    });
    
    // دالة تحريك الأرقام
    function animateNumber(element, start, end, duration) {
        const range = end - start;
        const increment = range / (duration / 16);
        let current = start;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= end) {
                current = end;
                clearInterval(timer);
            }
            
            // الحفاظ على النص الإضافي (مثل "DA")
            const originalText = element.textContent;
            const numberPart = Math.floor(current);
            const extraText = originalText.replace(/\d+/g, '');
            
            element.textContent = numberPart + extraText;
        }, 16);
    }
    
    // إضافة تأثير النبض للكروت المهمة
    const importantCards = document.querySelectorAll('.card-waiting, .card-pending-payments');
    
    importantCards.forEach(card => {
        const number = parseInt(card.querySelector('h2, h4').textContent) || 0;
        if (number > 0) {
            card.classList.add('pulse-animation');
        }
    });
    
    // تحديث الوقت والتاريخ
    updateDateTime();
    setInterval(updateDateTime, 1000);
    
    function updateDateTime() {
        const now = new Date();
        const timeElement = document.getElementById('current-time');
        const dateElement = document.getElementById('current-date');
        
        if (timeElement) {
            timeElement.textContent = now.toLocaleTimeString('fr-FR', {
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            });
        }
        
        if (dateElement) {
            dateElement.textContent = now.toLocaleDateString('fr-FR', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        }
    }
});

// إضافة CSS للتأثيرات
const style = document.createElement('style');
style.textContent = `
    .pulse-animation {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% {
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        50% {
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        }
        100% {
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
    }
    
    .dashboard-card {
        transition: all 0.3s ease !important;
    }
`;
document.head.appendChild(style);