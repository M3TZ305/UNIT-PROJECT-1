# 🤖 [AgentOSا] - Autonomous AI Agent & System OS (CLI)

> An advanced, interactive command-line interface (CLI) platform designed for managing, purchasing, and deploying AI agent clusters. Built with Python, featuring rich terminal UI, interactive menus, and modular software architecture.

---

## 📌 Project Overview

The **[AgentOSا]** platform is a futuristic terminal-based application that allows developers and administrators to browse, configure, purchase, and deploy autonomous artificial intelligence agents. The system features two distinct user roles: **Customers (Developers)** and **Managers (Administrators)**, ensuring full e-commerce and cluster management functionality.

---

## 👥 Features & User Stories

### As a Customer (Developer), I should be able to:

- **Browse Products:** View the available catalogue of AI agents and their specializations.
- **View Product Info:** Inspect deep specifications, success rates, token prices, and stock levels.
- **Search for Products:** Instantly search for specific AI agents by name or specialization keyword.
- **Get Recommendations:** Receive smart AI recommendations for the next deployment based on past history.
- **Add to Cart:** Select and add desired AI agents to the shopping cart.
- **Remove from Cart:** Modify the cart by removing unwanted agents.
- **List Cart Products:** View all items currently in the shopping cart with total token calculations.
- **Proceed to Checkout:** Complete purchases securely using platform tokens.
- **Fill Delivery Address:** Provide target cluster endpoint/IP addresses for deployment.
- **Get Purchase Receipt:** Receive an official digital receipt with transaction details.
- **Check Deployment Status:** Monitor real-time synchronization and deployment status of purchased agents.

### As a Manager (Administrator), I should be able to:

- **Access Manager Portal:** Securely log in using administrator credentials.
- **View Inventory & Stock:** Monitor active stock quantities and marketplace performance.
- **Register New Agents:** Add new AI models and agents to the live marketplace catalogue.

---

## 📂 Project Architecture (Modules & Packages)

The project follows a clean separation of concerns, organized into robust packages and modules:
agentos/
│
├── core/               # Core system logic & database
│   ├── __init__.py
│   └── database.py     # Local JSON state management
│
├── ui/                 # Visual interface & animations
│   ├── __init__.py
│   ├── animations.py   # Rich terminal spinners and banners
│   └── menus.py        # Interactive questionary menus and tables
│
├── services/           # Business logic & operations
│   ├── __init__.py
│   ├── store.py        # Cart, search, and recommendations
│   ├── checkout.py     # Payment processing and receipts
│   └── manager.py      # Administrator inventory control
│
├── main.py             # Main application entry point
├── requirements.txt    # Project Python dependencies
└── README.md           # Project documentation

---

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd agentos
   ```
2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application:**
   ```bash
   python main.py
   ```

## 🕹️ Usage Guide

When you run `python main.py`, an interactive terminal dashboard will launch. Use your keyboard Arrow Keys to navigate and Enter to select options:

- **Browse AI Agents Catalogue:** View all available AI agents in a structured rich table.
- **Search for an Agent:** Type keywords (e.g., Architecture, Security) to filter agents.
- **Get AI Recommendations:** Discover tailored agent suggestions for your infrastructure.
- **View My Cart & Checkout:** Manage your selected items, input your target IP/Endpoint, and execute deployment.
- **Track Deployment Status:** Review your active cluster node sync states.
- **Manager Portal:** Enter access key (1234) to manage inventory and register new agents.
