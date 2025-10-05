📦 StockPulse – Low Stock Alert System

Stop running out of stock — stay alert and restock smarter!
StockPulse is a simple yet efficient inventory management web application that helps shopkeepers and small businesses monitor product quantities, track purchase history, and receive instant low-stock alerts.

🧠 Project Overview

In small shops, keeping track of stock manually often leads to missed restocking and lost sales.
StockPulse solves this by providing:

Real-time product tracking

Automatic low-stock indication

Easy purchase recording and management

Built using Flask (Python) for backend and HTML/CSS/JavaScript for frontend, this system stores all inventory data locally using SQLite3.

🚀 Features

✅ Add, update, and delete products
✅ Automatic low-stock detection and alerts
✅ Maintain purchase history with timestamps
✅ Interactive and responsive web interface
✅ Local database storage (SQLite3)
✅ Simple setup — no external dependencies required

🛠️ Tech Stack
Component	Technology
Frontend	HTML, CSS, JavaScript
Backend	Flask (Python)
Database	SQLite3
Design	Poppins font, Tailored minimal UI
⚙️ Installation & Setup

Follow these steps to run the project locally 👇

1️⃣ Clone the Repository
git clone https://github.com/jignesh0318/First-Project
cd StockPulse

2️⃣ Create a Virtual Environment
python -m venv venv
venv\Scripts\activate    # On Windows
# OR
source venv/bin/activate # On macOS/Linux

3️⃣ Install Required Dependencies
pip install flask

4️⃣ Run the Application
python app.py

5️⃣ Open in Browser

Go to 👉 http://127.0.0.1:5000

(To access from phone: use your laptop’s IP and open http://<your-laptop-ip>:5000)

🗂️ Folder Structure
StockPulse/
│
├── app.py                # Flask backend
├── stock.db              # SQLite3 database (auto-created)
├── templates/
│   └── index.html        # Frontend HTML
├── static/
│   └── style.css         # Stylesheet
└── README.md             # Project documentation

💡 How It Works

Add a new product with its name, quantity, and threshold limit.

The system displays whether the stock is OK ✅ or Low ⚠️ based on the threshold.

When a product is sold or used, record the purchase — stock updates automatically.

View purchase history with timestamps in the Purchase section.

🧩 Future Enhancements

🚀 Add authentication (login for shop owners)
📊 Include stock analytics and charts
📱 Create a mobile-friendly dashboard
📤 Enable Excel/CSV data export

👨‍💻 Developer

Jignesh Tendulkar
📧 tendulkarjignesh1@gmail.com

🖥️ GitHub: github.com/jignesh0318

📝 License

This project is open-source and available under the MIT License.