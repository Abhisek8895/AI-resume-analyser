# AI Resume Analyzer

An AI-powered **Streamlit** application that evaluates a resume against a job description using **semantic similarity**, performs **ATS-style resume analysis**, identifies **missing skills**, checks **resume structure**, detects **weak bullet points**, and uses an **LLM (Groq + LangChain)** to rewrite weak resume bullets.

---

## ✨ Features

### 📄 PDF Resume Parsing
- Upload resumes in **PDF** format
- Extracts text using **PyPDF2**

### 🎯 AI Job Match Score
- Compares the resume with the job description using **sentence embeddings**
- Uses the **all-MiniLM-L6-v2** Sentence Transformer model
- Calculates similarity with **Cosine Similarity**
- Goes beyond simple keyword matching

### 📊 ATS Grade & Feedback
Converts the semantic similarity score into an ATS-style grade.

| Score | Grade |
|--------|-------|
| < 40 | Poor |
| 40 – 59 | Average |
| 60 – 74 | Good |
| 75 – 89 | Very Good |
| 90+ | Excellent |

Provides human-readable feedback explaining the result.

### 🛠 Skill Matching
- Extracts skills from both the resume and job description
- Uses a curated skill database
- Highlights:
  - Matching skills
  - Missing skills
  - Resume-only skills

### 📑 Resume Structure Analysis
Checks whether the resume contains important sections such as:

- Experience
- Education
- Skills
- Projects
- Certifications (optional)

Also detects:

- Email
- Phone Number

Warns if important sections or contact information are missing.

### ✍️ Resume Bullet Quality Analysis
Analyzes Experience and Projects sections.

Flags bullets that:

- start with weak phrases such as
  - worked on
  - responsible for
  - helped
  - involved in
- do not contain measurable achievements
- lack quantifiable metrics

### 🤖 AI Bullet Rewriting
Uses **Groq + LangChain** to rewrite weak resume bullets into stronger achievement-oriented statements with a single click.

---

# 🧰 Tech Stack

| Category | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Language | Python |
| PDF Parsing | PyPDF2 |
| Embeddings | sentence-transformers |
| Similarity | scikit-learn (Cosine Similarity) |
| LLM | Groq |
| Framework | LangChain |
| Environment Variables | python-dotenv |
| Resume Analysis | Python + Regex |

---

# 📂 Project Structure

```
AI-Resume-Analyzer/
│
├── app.py                 # Streamlit application
├── analyzer.py            # Resume-JD similarity scoring
├── skills.py              # Skill extraction & matching
├── sections.py            # Resume section detection
├── contact.py             # Email & phone detection
├── quality.py             # Bullet quality analysis
├── rewrite.py             # LLM-powered bullet rewriting
├── utils.py               # Utility functions
├── requirements.txt
├── .env
└── README.md
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/Abhisek8895/AI-Resume-Analyzer.git

cd AI-Resume-Analyzer
```

---

## 2. Create a Virtual Environment (Optional)

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Get a Groq API Key

Create a free API key from

https://console.groq.com

---

## 5. Create a `.env` File

```env
GROQ_API_KEY=your_api_key_here
```

---

## 6. Run the Application

```bash
streamlit run app.py
```

---

# 🚀 Usage

1. Launch the Streamlit application.
2. Upload a PDF resume.
3. Review the resume structure analysis.
4. Paste the job description.
5. Click **Run Analysis**.
6. Review:
   - Match Score
   - ATS Grade
   - ATS Feedback
   - Skill Match
   - Missing Skills
   - Resume Structure
   - Weak Resume Bullets
7. Click **Rewrite this** for AI-generated improvements.

---

# 🧠 How the AI Match Score Works

Instead of relying only on keyword matching, the application compares the overall meaning of the resume and job description.

### Step 1
The resume text is converted into a sentence embedding using:

```
all-MiniLM-L6-v2
```

### Step 2

The job description is converted into another embedding using the same model.

### Step 3

The two embeddings are compared using **Cosine Similarity**.

### Step 4

The similarity score is converted into a percentage (0–100).

### Step 5

The percentage is mapped to an ATS grade.

| Score | Grade | Feedback |
|--------|-------|----------|
| <40 | Poor | Resume is not aligned with the job role. |
| 40–59 | Average | Partial match. Improve skills and projects. |
| 60–74 | Good | Good match with room for improvement. |
| 75–89 | Very Good | Strong alignment with the job description. |
| 90+ | Excellent | Highly relevant profile for the role. |

---

# 📦 Requirements

```
streamlit
PyPDF2
sentence-transformers
scikit-learn
langchain==1.3.11
langchain-groq==1.1.3
python-dotenv==1.2.2
```

Or install using:

```bash
pip install -r requirements.txt
```

---

# ⚠️ Known Limitations

- Supports **PDF resumes only**.
- DOCX support is not implemented.
- Resume section detection is heuristic-based and depends on common section headings.
- Multi-column resumes may not always be parsed correctly because PyPDF2 does not preserve layout information.
- ATS formatting checks (tables, graphics, icons, text boxes) are not currently supported.
- Skill extraction relies on a predefined skill database.

---

# 🔮 Future Improvements

- DOCX resume support
- Multiple resume comparison
- Resume keyword optimization
- ATS formatting score
- Resume grammar checking
- Cover letter generation
- Resume improvement suggestions
- Recruiter dashboard
- Resume history
- Export analysis as PDF
- Custom skill database
- Support for multiple LLM providers (Gemini, OpenAI, Claude)

---

# 👨‍💻 Author

**Abhisek Mishra**

Aspiring AI/ML Engineer | Generative AI | Machine Learning | Python Developer

- LinkedIn: https://www.linkedin.com/in/abhisek-mishra-
- GitHub: https://github.com/Abhisek8895

---

# 📄 License

This project is licensed under the MIT License.

Feel free to fork, modify, and use it for learning purposes.

---

## ⭐ If you found this project useful, consider giving it a star on GitHub!
