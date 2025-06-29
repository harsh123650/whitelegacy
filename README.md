# 🐄 White Legacy – Dairy Farm Web App

**White Legacy** is a comprehensive dairy farm management web application built using Django. It is designed to manage all aspects of a modern dairy business, from administration and staff coordination to worker inputs and customer subscription tracking. The platform ensures smooth operations, transparency, and digital record-keeping for every milk delivery and buffalo activity.

---

## 🌐 Live Demo

[Visit Now](https://whitelegacy.onrender.com)

---

## 🏠 Homepage

* Custom landing page with a fixed navbar, hero section, feature highlights, and contact form.
* Internal CSS for styling with sections like Delivery Process, Products, Our Guarantee, and Customer Testimonials.
* 'Start' button redirects to secure login.

---

## 🔐 User Roles & Dashboards

### 👑 Admin Panel

* Hardcoded admin credentials: `Harshal123 / Harshal@123`
* Auto-create admin if not present.
* Sidebar-based dashboard with the following features:

  * 📋 View all registered Staff, Workers, and Customers
  * ➕ Create Staff / Worker / Customer with auto-generated IDs (S001, W001, C001)
  * ❌ Delete any user
  * 🥛 View all Milk Delivery Logs (filterable by date)
  * 🐃 View all Buffalo Milking Logs (filterable by date)
  * 📬 View Contact Us form entries
  * 📩 View Subscription form entries
  * 💳 View Payment data (filtered by Monthly, Quarterly, Yearly plans)

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

---

### 👤 Customer Panel

* Sidebar layout with 5 sections:

  1. 🏠 Home – Shows active subscription (start & end date)
  2. 📅 My Deliveries – Daily milk status entries with time
  3. 📲 UPI Payment – Scan QR and make payment
  4. 🏦 Other Payment – Opens custom secure payment form
  5. 🚪 Logout
* Subscription selector with options:

  * Monthly
  * Quarterly
  * Yearly
* Upon payment:

  * Subscription dates are calculated and saved
  * Displayed dynamically in dashboard

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

---

## 📧 Contact

* Email: [whitelegacy.dairy@gmail.com](mailto:whitelegacy.dairy@gmail.com)
* GitHub: [Your GitHub Link](https://github.com/yourusername/whitelegacy)
* Project Manager: Harshal Patil

---

## 🪪 License

This project is licensed under the MIT License.

---

> Designed with ❤️ to revolutionize traditional dairy management. Powered by Django and inspired by Indian dairy innovation.
