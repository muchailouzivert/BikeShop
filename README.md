# Bike Shop

## Мета
Демонстрація використання шаблонів проєктування (Builder, Facade, Strategy) у Django-проєкті для оренди велосипедів. Основний функціонал включає реєстрацію/авторизацію користувача, замовлення велосипедів (електричних або звичайних), скасування/пітдтвердження замовлень,  відправку email-повідомлень.

---

## Використані шаблони проєктування

### 1. **Builder (Генеративний)**
**Мета:** Побудова об’єкта `Bike` з поетапним налаштуванням параметрів.  
**Файли:** `services.py`

- `BikeBuilder` – базовий клас-будівельник.
- `RegularBikeBuilder`, `ElectricBikeBuilder` – конкретні реалізації для відповідних типів велосипедів.
- `BikeDirector` – контролює процес побудови.

📌 **Перевага**: Легко змінювати конфігурацію велосипеда без зміни клієнтського коду.

---

### 2. **Facade (Структурний)**
**Мета:** Спрощення взаємодії з підсистемами (замовлення велосипедів, аутентифікація).  
**Файли:** `bike_views.py`, `user_views.py`

- `BikeFacade` – інтерфейс для створення замовлення.
- `UserFacade` – реєстрація, логін, лог-аут користувача + email-нотифікації, керування статусом замовлень(прийняти або скасувати).

📌 **Перевага**: Спрощення інтерфейсу для контролерів, централізація логіки.

---

### 3. **Strategy (Поведінковий)**
**Мета:** Надання гнучкості у виборі способу повідомлення.  
**Файли:** `notifications/`

- `NotificationStrategy` – інтерфейс.
- `EmailNotificationStrategy` – реалізація через email.
- `NotifierContext` – контекст, який викликає конкретну стратегію.

📌 **Перевага**: Легко додавати інші способи повідомлень.

---
## Застосування дизайн принців
🔹**SOLID**

**S — Single Responsibility Principle**

- Кожен клас має одну чітко визначену відповідальність:

- UserFacade — логіка реєстрації, входу, виходу, email-сповіщень та управління замовленнями.

- BikeFacade — створення велосипеда та пов’язаного замовлення.

- BikeBuilder / ElectricBikeBuilder / BikeDirector — побудова об'єкта Bike.

- NotifierContext — виконує лише функції сповіщення.

**O — Open/Closed Principle**

- Код відкритий до розширення, але закритий до модифікації:

- Додати новий тип велосипеда можна, реалізувавши новий клас Builder.

- Додати нову стратегію сповіщень — просто підключити нову стратегію без зміни існуючого коду.

**L — Liskov Substitution Principle**

- Усі підкласи BikeBuilder (наприклад, ElectricBikeBuilder) можуть використовуватись замість базового класу без порушення логіки.

**I — Interface Segregation Principle**

- Класи реалізують лише ті методи, які їм потрібні. Немає зайвих або порожніх методів.

**D — Dependency Inversion Principle**

- UserFacade працює з абстракцією NotifierContext, а не напряму з EmailNotificationStrategy.

- BikeDirector отримує Builder як залежність, що дозволяє легко підмінювати реалізацію.

🔹 **KISS — Keep It Simple, Stupid**

- Мінімальна логіка в контролерах — обробку делеговано фасадам (UserFacade, BikeFacade).

- Прості умови, зрозуміла структура, мінімум вкладеності.

- Зрозуміле розділення відповідальностей між компонентами системи.

## Тестування

У проекті реалізовано понад **20 модульних тестів**:

- `test_builder.py` – тести для Builder.
- `test_facade_user.py` – тести для UserFacade.
- `test_facade_bike.py` – тести для BikeFacade.
- `test_strategy.py` – тести для стратегії нотифікацій.
- `test_main_views.py` – інтеграційне тестування для основних контролерів.

Команда запуску:
```
python manage.py test
