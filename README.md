# 🚀 AI Resume Tailor

AI Resume Tailor is a modern web application that helps you instantly tailor your LaTeX (or PDF) resume to any job description using AI. Upload your resume, paste a job description, and get a customized, ATS-friendly resume in seconds—with options to download as LaTeX or PDF.

---

## ✨ Features
- Upload your resume in **LaTeX (.tex)** or **PDF** format
- Paste any job description
- AI-powered tailoring: aligns your resume content to the job description (no fake skills added!)
- Download the tailored resume as **LaTeX** or **PDF**
- Beautiful, modern UI with Ant Design
- FastAPI backend with OpenAI/GPT integration

---

## 🖼️ Screenshots
<!--
Add screenshots here after running the app!

![Home Page](screenshots/home.png)
![Tailored Resume](screenshots/result.png)
-->

---

## 🛠️ Tech Stack
- **Frontend:** React, Ant Design, Axios
- **Backend:** FastAPI, Python, spaCy, OpenAI GPT, pdflatex

---

## ⚡ Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YaswanthRDasari/AI-Resume-Tailor.git
cd AI-Resume-Tailor
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
# Set up your .env file with OpenAI/Azure credentials
uvicorn app.main:app --reload
```

### 3. Frontend Setup
```bash
cd ../frontend
npm install
npm start
```

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend: [http://localhost:8000](http://localhost:8000)

---

## 🚦 Usage
1. Upload your LaTeX or PDF resume
2. Paste the job description
3. Click **Tailor My Resume**
4. Download the tailored LaTeX or PDF resume

---

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License
[MIT](LICENSE)

---

> Made with ❤️ by Yaswanth Reddy Dasari 