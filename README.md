<div align="center">

# 🏦 Online Banking System

### A comprehensive, secure, and feature-rich online banking platform

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)](https://www.sqlite.org/)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Security Features](#-security-features)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

The **Online Banking System** is a full-featured banking platform built with Flask that provides a complete digital banking experience. The system supports multiple account types, lending services, investment options, and advanced security features including two-factor authentication (2FA).

This platform is designed to simulate real-world banking operations with features like automated EMI processing, credit card management, bulk payment handling, and comprehensive transaction tracking with email notifications.

---

## ✨ Features

### 🏠 Account Management
- **Multiple Account Types**: Support for Savings and Current accounts
- **User Authentication**: Secure signup/login with password hashing
- **Two-Factor Authentication (2FA)**: Enhanced security with OTP verification
- **Account Dashboard**: Real-time balance, transaction history, and analytics
- **Profile Management**: Update personal information and account details
- **Debit Card Management**: Create and manage debit cards with PIN protection

### 💸 Banking Operations
- **Deposits & Withdrawals**: Quick and secure fund transfers
- **Money Transfers**: Transfer funds between accounts
- **Bulk Payments**: Upload CSV/Excel files for multiple transactions
- **GST & Tax Payments**: Dedicated portal for tax payments
- **Transaction History**: Comprehensive transaction logs with filtering
- **Account Statements**: Download statements in multiple formats

### 💳 Credit Services
- **Credit Cards**: Apply for and manage multiple credit cards
- **Credit Card Purchases**: Make purchases using credit cards
- **Payment Processing**: Pay credit card bills and track statements
- **Credit Card Statements**: View detailed transaction history
- **Multiple Card Support**: Manage various card types with different limits

### 💰 Loan Services
- **Personal Loans**: Apply for personal loans with flexible terms
- **Home Loans**: Long-term home financing options
- **Business Loans**: Commercial lending for business needs
- **Automated EMI Processing**: Scheduled monthly EMI deductions
- **Loan Dashboard**: Track all loans, EMIs, and payment schedules
- **Early Closure**: Option to close loans before maturity

### 📈 Investment Options
- **Fixed Deposits (FD)**: Secure investments with guaranteed returns
- **Recurring Deposits (RD)**: Regular savings with compounding interest
- **Mutual Funds**: Investment in market-linked mutual funds
- **Investment Dashboard**: Track all investments and returns
- **Maturity Notifications**: Email alerts for maturity dates
- **Liquidation Options**: Withdraw investments before maturity

### 🔒 Security & Notifications
- **Password Encryption**: Secure password hashing using industry standards
- **CSRF Protection**: Protection against cross-site request forgery
- **Session Management**: Secure session handling and timeout
- **Email Notifications**: Automated emails for all transactions
- **Transaction Alerts**: Real-time notifications for account activities
- **Low Balance Alerts**: Automatic warnings and charges

---

## 📸 Screenshots

### Dashboard & Account Overview
<img width="1582" alt="Dashboard - Account Overview" src="https://github.com/user-attachments/assets/c3809e66-78b6-4a56-9c07-554244826221" />

*Main dashboard showing account balance, recent transactions, and quick action buttons*

---

### Banking Operations
<img width="1582" alt="Deposit Funds" src="https://github.com/user-attachments/assets/2fffb655-8891-458a-a7fa-6a4e40d06139" />

*Deposit interface for adding funds to your account*

---

<img width="1582" alt="Money Transfer" src="https://github.com/user-attachments/assets/8c119526-680a-4185-ab56-91f4a01cb3fe" />

*Transfer money to other accounts with real-time validation*

---

### Credit Card Management
<img width="1582" alt="Credit Card Application" src="https://github.com/user-attachments/assets/a8098bcf-d97b-40c5-bd4c-1abbe846d6ce" />

*Apply for credit cards with instant approval system*

---

<img width="1582" alt="Credit Card Dashboard" src="https://github.com/user-attachments/assets/22b25186-8cc0-4e47-b1df-453eb0536903" />

*View and manage all your credit cards in one place*

---

### Loan Services
<img width="1582" alt="Loan Application" src="https://github.com/user-attachments/assets/5e68f282-1615-4962-851e-f834a4b75871" />

*Apply for various types of loans with flexible terms*

---

<img width="1582" alt="My Loans Dashboard" src="https://github.com/user-attachments/assets/4490ffbf-bee6-4b86-a94e-5d0255e81227" />

*Track all your loans, EMIs, and outstanding balances*

---

### Investment Portfolio
<img width="1582" alt="Investments Overview" src="https://github.com/user-attachments/assets/5e70f949-bc89-4401-afe7-faf215dce554" />

*Investment dashboard showing FD, RD, and mutual fund holdings*

---

<img width="1582" alt="Fixed Deposit" src="https://github.com/user-attachments/assets/7e0395bb-1eb8-418f-87fe-16baf0c35996" />

*Create fixed deposits with customizable tenure and interest rates*

---

### Advanced Features
<img width="1582" alt="Bulk Payments" src="https://github.com/user-attachments/assets/b03c419d-f446-4364-9d77-0c82e92dd08f" />

*Upload CSV/Excel files for processing multiple payments at once*

---

<img width="1582" alt="Two-Factor Authentication" src="https://github.com/user-attachments/assets/07dcf386-6a90-4f06-86ad-69a0be3d5c8c" />

*Enable 2FA for enhanced account security with QR code setup*

---

<img width="1582" alt="Transaction History" src="https://github.com/user-attachments/assets/7d84f2f8-9277-4b6a-a2d0-16b3c56b0505" />

*Comprehensive transaction history with filtering and search capabilities*

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 2.0+
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Werkzeug security (password hashing)
- **2FA**: PyOTP for OTP generation
- **Scheduler**: APScheduler for automated tasks

### Frontend
- **Template Engine**: Jinja2
- **Styling**: Custom CSS
- **Icons & UI**: Modern responsive design

### Libraries & Tools
- **Email**: Flask-Mail for notifications
- **Security**: Flask-WTF for CSRF protection
- **Data Processing**: OpenPyXL for Excel, CSV for bulk operations
- **QR Code**: qrcode library for 2FA setup

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/GarvRandhar/Online-Banking-System.git
   cd Online-Banking-System
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask flask-sqlalchemy flask-mail pyotp qrcode werkzeug apscheduler openpyxl
   ```

4. **Initialize the database**
   ```bash
   python init_db.py
   ```

5. **Configure environment variables** (optional)
   ```bash
   export SECRET_KEY='your-secret-key-here'
   export MAIL_USERNAME='your-email@gmail.com'
   export MAIL_PASSWORD='your-app-password'
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   - Open your browser and navigate to `http://localhost:5000`
   - Create a new account using the signup page
   - Start exploring the banking features!

---

## 📖 Usage

### Creating an Account
1. Navigate to the signup page
2. Fill in your personal details (name, DOB, email, phone, address)
3. Set an initial deposit amount (minimum required)
4. Create a secure password
5. Submit and receive your unique account number

### Basic Operations
- **Deposit**: Add funds to your account instantly
- **Withdraw**: Remove funds (subject to available balance)
- **Transfer**: Send money to other account holders
- **Check Balance**: View real-time account balance

### Advanced Features
- **Apply for Loans**: Choose from personal, home, or business loans
- **Credit Cards**: Apply and manage credit cards
- **Investments**: Create FD, RD, or invest in mutual funds
- **Bulk Payments**: Upload Excel/CSV files for multiple transactions
- **2FA Setup**: Enable two-factor authentication for added security

---

## 📁 Project Structure

```
Online-Banking-System/
├── app.py                 # Main application file with routes
├── models.py              # Database models (Account, Transaction, etc.)
├── api.py                 # API endpoints (if any)
├── investments.py         # Investment management logic
├── security.py            # Security utilities
├── init_db.py            # Database initialization script
├── database.db           # SQLite database (created after init)
├── templates/            # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   ├── signup.html
│   └── ...
└── static/              # Static files (CSS, JS, images)
    └── styles.css
```

---

## 🔐 Security Features

- **Password Hashing**: All passwords are hashed using Werkzeug's security module
- **CSRF Protection**: Flask-WTF provides CSRF token validation
- **Session Security**: Secure session management with timeouts
- **Two-Factor Authentication**: Optional 2FA using time-based OTP
- **Input Validation**: Server-side validation for all user inputs
- **SQL Injection Prevention**: SQLAlchemy ORM prevents SQL injection
- **Secure Email**: Encrypted SMTP for email notifications

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Guidelines
- Follow PEP 8 style guide for Python code
- Write clear commit messages
- Add comments for complex logic
- Test your changes thoroughly

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact

**Garv Randhar**

- GitHub: [@GarvRandhar](https://github.com/GarvRandhar)
- Repository: [Online-Banking-System](https://github.com/GarvRandhar/Online-Banking-System)

---

<div align="center">

### ⭐ If you found this project helpful, please consider giving it a star!

**Made with ❤️ using Flask**

</div>
