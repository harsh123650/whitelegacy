#  White Legacy – The White Revolution 2.0

**White Legacy** is a comprehensive smart dairy web application built using Django. It is designed to manage all aspects of a modern dairy business, from administration and staff coordination to worker inputs and customer subscription tracking. The platform ensures smooth operations, transparency, and digital record-keeping for every milk delivery and buffalo activity.

---
![Home Page](Home%20Page.png)

## 🌍 [Live Demo](https://whitelegacy.onrender.com)

Click the link above to explore our products, know our story, and understand our process on the White Legacy.


---
> 🧩 **WhiteLegacy is not a multi-tenant platform.**  
> It functions as a dedicated management system for **one farm**, handling all roles (admin, staff, worker, customer) in a closed environment.

---
## 🏠 Homepage

* Custom landing page with a fixed navbar, hero section, feature highlights.
* Internal CSS for styling with sections like Delivery Process, Products, Our Guarantee, and Customer Testimonials.
* 'Start' button redirects to secure login.

---
### 📘 About Us
Learn about the mission and journey of our dairy farm. The About Us page highlights our passion for fresh, organic milk and our commitment to reaching every doorstep with quality and care.

### 📝 Subscribe Form
Visitors can subscribe for updates, special offers, or plan information. Admins can view and manage all subscriber data through the dashboard.

### 📚 User Guide
Step-by-step walkthrough for new users explaining login, dashboard access, milk delivery logging, buffalo health updates, and subscription process.

### 📞 Contact Us
A form-based communication channel for users to reach out. Messages are securely stored and displayed to the admin.

### 📲 Social Media Integration
Stay connected with us on Instagram, Facebook, and LinkedIn. Social icons are visible in the footer for quick access.

---
## 🔐 User Roles & Dashboards

### 👑 Admin Panel

* Hardcoded admin credentials: `Harshal123 / Harshal@123`
* Auto-create admin if not present.
* Sidebar-based dashboard with the following features:

  * 📋 View all registered Staff(delivery), Workers, and Customers.
  * ➕ Create Staff(Delivery) / Worker / Customer with auto-generated IDs (S001, W001, C001).
  * ❌ Delete any user.
  * 🥛 View all Milk Delivery Logs (filterable by date).
  * 🐃 View all Buffalo Milking Logs (filterable by date).
  * 📬 View Contact Us form entries.
  * 📩 View Subscription form entries.
  * 💳 View Payment data (filtered by Monthly, Quarterly, Yearly plans) and also download invoice.

---

### 👩‍💼 Staff Panel (Milk Delivery)

* View list of all customers
* Update milk delivery status for customers
* Add delivery time and date for each customer
* Automatically visible in customer dashboard and admin logs

---

### 🧑‍🌾 Worker Panel (Buffalo Health & Milking)

* Submit buffalo number
* Enter quantity of milk (morning & evening)
* Add remarks for health check
* Select date of entry
* Admin can monitor all logs daily
* It helps in maintaining cattle health and dry period 

---

### 👤 Customer Panel

* Sidebar layout with 5 sections:

  1. 🏠 Home – Shows active subscription (start & end date)
  2. 📅 My Deliveries – Daily milk status entries with time
  3. 📲 UPI Payment – Scan QR and make payment
  4. 🏦 Other Payment – Opens custom secure payment form
  5. 🚪 Logout

### 💰 Subscription-Based Strategy

WhiteLegacy implements a **subscription-driven model** where customers can choose from flexible milk delivery plans:

- **Monthly Plan**
- **Quarterly Plan**
- **Yearly Plan**

Upon choosing a plan, the system:
- Automatically records the **start and end date** of the subscription
- Shows it in the **customer dashboard**
- Enables delivery tracking for subscribed periods only
- Integrates a basic **Razorpay Gateway** and a **testing-based payment option** for demo purposes

This strategy simulates a real-world business approach used by modern dairy brands and milk delivery apps. A full payment gateway integration is planned for future development.

* Upon payment:

  * Subscription dates are calculated and saved
  * Displayed dynamically in dashboard
  * They also download payment invoice


---

## 💻 Technical Overview

### ⚙️ Technologies Used

* **Frontend**: HTML5, CSS3, Bootstrap 5, Font Awesome, Chart.js
* **Backend**: Python 3.13, Django 5.2.3
* **Database**: SQLite3
* **Hosting**: Render.com

### 🗂️ Project Structure

```
milkapp_project/
├── dairyapp/
│   ├── migrations/
│   ├── static/
│   │   └── dairyapp/css/
│   │       └── login.css, index.css, admin.css, etc.
│   ├── templates/
│   │   └── dairyapp/
│   │       ├── index.html
│   │       ├── login.html
│   │       ├── admin.html
│   │       ├── staff.html
│   │       ├── worker.html
│   │       ├── customer.html
│   │       ├── payment.html
│   │       ├── about.html
│   │       ├── subscription_select.html
│   │       └── ...
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
├── db.sqlite3
├── manage.py
└── README.md
```

---

## 🧑‍💻 Setup Instructions

1. **Clone the repository**:

```bash
git clone https://github.com/yourusername/whitelegacy.git
cd whitelegacy
```

2. **Create virtual environment**:

```bash
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Apply migrations**:

```bash
python manage.py migrate
```

5. **Start the server**:

```bash
python manage.py runserver
```

6. **Visit app in browser**:
   [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📋 Admin Credentials

```
Username: Harshal123
Password: Harshal@123
```

* Admin account is automatically created if not found on login.
You also use some credentials which currently run:
customer :
username:cust3
password:cust123

staff:
username:staff3
password:staff3

worker:
username:worker3
password:worker3

---

## 📧 Contact

* Email: [whitelegacy.dairy@gmail.com](mailto:whitelegacy.dairy@gmail.com)
* GitHub: [Your GitHub Link](https://github.com/yourusername/whitelegacy)
* Project Manager: Harshal Patil

---

## 🪪 License

This project is licensed under the MIT License.

---

> ❤️ WhiteLegacy aims to **revolutionize the Indian dairy ecosystem** — just like **Jio transformed India's digital landscape**, this project represents **White Revolution 2.0**, empowering dairy operations with smart digital tools.
