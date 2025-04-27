![github-submission-banner](https://github.com/user-attachments/assets/a1493b84-e4e2-456e-a791-ce35ee2bcf2f)

# 🚀 Stock Sense AI
Your AI-powered stock market research assistant — fast, intelligent, and beginner-friendly.

---

## 📌 Problem Statement
**Problem Statement** – Build a stock market assistant using Groq to help both beginners and experts automate their tasks.

---

## 🎯 Objective
Accessing stock market insights today requires users to visit multiple websites for trends, comparisons, and news, making the process time-consuming and inefficient.  
**Stock Sense AI** provides a single AI-powered platform that automates research, offers real-time data, and simplifies decision-making for both beginners and experts.

---

## 🧠 Team & Approach

**Team Name:** AI Hunter

**Team Members:**
- [Pranav Nalawade](https://github.com/PlanetDestroyyer) – AI Developer
- [Sahana Durgekar]() - Backend Developer
- [Harshita Singhal]() - Frontend Developer

**Our Approach:**
- We chose this problem because financial research is complicated, especially for beginners.
- **Key challenges addressed:**
  - Fetching, structuring, and summarizing stock data in a user-friendly way.
  - Integrating Groq LLM to answer finance-related queries quickly.
  - Building a clean, simple web interface for users of all levels.
- **Pivots and breakthroughs:**
  - Switched to Flask for rapid prototyping and easier deployment.
  - Tuned LLM prompts for structured outputs.
  - Optimized data fetching for faster performance.

---

## 🛠️ Tech Stack

**Core Technologies Used:**
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Flask (Python)
- **Database:** None (dynamic/live data fetching)
- **APIs:** 
  - Groq API for natural language understanding
  - Finviz page for stock news and data

**Sponsor Technologies Used:**
- **Groq:** Used to process stock-related questions and provide AI-powered insights.

---

## ✨ Key Features

✅ Ask any stock market-related query powered by Groq  
✅ View real-time stock summaries and news in one place  
✅ Beginner-friendly UI with simple navigation  
✅ Automated research — save hours of manual searching  

---

## 📽️ Demo & Deliverables

- **Live Hosting Link:** [https://stock-sense-ai.onrender.com/](https://stock-sense-ai.onrender.com/)
- **Demo Video Link:** [Paste YouTube or Loom link here]
- **Pitch Deck / PPT Link:** [Paste Google Slides / PDF link here]

---

## ✅ Tasks & Bonus Checklist

- ✅ All team members followed the required social channels and filled the form.
- ✅ Bonus Task 1: Shared badges and filled the form (2 points)
- ✅ Bonus Task 2: Signed up for Sprint.dev and filled the form (3 points)

---

## 🧪 How to Run the Project

**Requirements:**
- Python 3.10+
- Flask
- API key for Groq (add in `.env` file)

**Local Setup:**
```bash
# Clone the repo
git clone https://github.com/PlanetDestroyyer/stock-sense-ai

# Navigate to project folder
cd stock-sense-ai

# Install dependencies
pip install -r requirements.txt

# Start Flask server
python app.py

```
## 🧬 Future Scope

- 📈 Develop it into a full SaaS product for financial research
- 🛡️ Add authentication and enhance data security
- 🌐 Add multi-language support for global accessibility
- 🔔 Add real-time alert notifications for stock trends
- 📊 Build personalized dashboards based on user preferences
- 📚 Integrate more detailed educational content for beginners

---

## 🧩 Challenges We Ran Into

**Context Length Issues:**  
We faced problems with context length as the tools were generating large amounts of text, which our models couldn’t process efficiently. To solve this, we experimented with different models that could handle longer or structured inputs better.

**Data Fetching for Top Movers:**  
While building the "Top Movers" page, fetching the top gainers and losers was taking a lot of time. To optimize performance, we added a filter to display only stocks that had moved up by 20% or more, ensuring faster and smoother loading.

**LLM Output Formatting:**  
Initially, the LLM was not providing answers in the correct Pydantic format. After tuning the prompt carefully, we managed to get the model to respond consistently in the expected structured format.

---

## 📎 Resources / Credits

- [Groq API Documentation](https://groq.dev/docs)
- [LangChain Documentation](https://docs.langchain.com/)
- [Finviz](https://finviz.com/) — For financial data and stock news

---

## 🏁 Final Words

Building Stock Sense AI was an exciting journey! 🚀  
We learned how to integrate LLMs with traditional frameworks like Flask, manage live stock data, and optimize performance for a smooth user experience.  
We also gained insights into prompt engineering, data structuring, and real-time application challenges.  
Huge thanks to the organizers, mentors, and sponsors for making this hackathon a great learning experience! 🙌

---
