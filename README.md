# 💰 Financial Advisor & Expense Manager AI

An AI-powered personal finance assistant that helps users track expenses, analyze spending habits, and receive personalized financial advice based on trusted financial philosophies. The system combines OCR, expense categorization, and Retrieval-Augmented Generation (RAG) to create a smart wealth management assistant.

---

## 🚀 Features

* 📷 Upload payment screenshots for automatic expense extraction
* 🔍 OCR-based text recognition from payment receipts
* 💳 Import bank statements and expense data
* 🗂️ Automatic expense categorization
* 📊 Interactive financial dashboard with spending insights
* 📚 Upload financial books and documents
* 🤖 AI-powered financial advisor using RAG
* 🎯 Personalized budgeting and saving recommendations
* 📈 Monthly expense analysis and reports

---

## 🛠️ Tech Stack

### Frontend

* Streamlit
* Plotly

### Backend

* Python
* Pandas
* SQLite / Firebase

### AI

* LangChain
* Gemini/OpenAI API
* FAISS / ChromaDB
* Sentence Transformers

### OCR

* Tesseract OCR
* Google Vision OCR (Optional)

---

## 📂 Project Structure

```text
FinancialAdvisorAI/
│
├── frontend/
│   ├── app.py
│   ├── dashboard.py
│   └── pages/
│
├── backend/
│   ├── ocr/
│   ├── expense_parser/
│   ├── bank_statement/
│   └── splitwise/
│
├── ai/
│   ├── rag/
│   ├── chatbot/
│   ├── prompts/
│   └── embeddings/
│
├── database/
│
├── uploads/
│   ├── books/
│   ├── screenshots/
│   └── statements/
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

```bash
git clone https://github.com/your-username/FinancialAdvisorAI.git

cd FinancialAdvisorAI

pip install -r requirements.txt

streamlit run frontend/app.py
```

---

## 📅 Development Roadmap

* **Week 1:** Project setup, planning, and environment configuration
* **Week 2:** OCR implementation and AI setup
* **Week 3:** Expense categorization and dashboard development
* **Week 4:** RAG integration for financial advice
* **Week 5:** Bank statement and expense analysis
* **Week 6:** Dashboard improvements and testing
* **Week 7:** Integration and bug fixes
* **Week 8:** Deployment and final presentation

---

## 👥 Team Responsibilities

### Member 1 – AI & Financial Advisor

* LangChain integration
* RAG implementation
* Financial chatbot
* Personalized financial recommendations

### Member 2 – OCR & Expense Analysis

* OCR pipeline
* Expense extraction
* Bank statement processing
* Expense categorization

### Member 3 – Frontend & Dashboard

* Streamlit interface
* Dashboard development
* Data visualization
* Deployment

---

## 🎯 Future Enhancements

* Splitwise API integration
* Budget alerts and notifications
* Investment tracking
* Goal-based savings planner
* Multi-user authentication
* Mobile-friendly interface

---

## 📄 License

This project is developed as part of an academic team project for learning purposes.

---

## ⭐ Acknowledgements

* LangChain
* Streamlit
* FAISS
* Tesseract OCR
* Google Gemini / OpenAI APIs

If you find this project useful, consider giving it a ⭐ on GitHub!
