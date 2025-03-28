# 🌐 Real-Time Translation API

## 📖 Overview

This project is a **Real-Time Translation API** built with **FastAPI**, designed to:
- Translate English text to Spanish using Google Translate.
- Generate a **reference translation** using Hugging Face’s `facebook/m2m100_418M` model.
- Evaluate the **BLEU score** and **Perplexity** of the translation.
- Monitor and return key **performance metrics** such as request count and memory usage.

---

## 👥 Users

This API is designed for:
- **Language learners**: who want to evaluate translation quality in real-time.
- **Developers & Researchers**: who need automated translation + NLP metrics.
- **Educators**: to demonstrate language model evaluation and monitoring.

---

## 🚀 Features

- ✅ Translate English to Spanish in real-time
- 📊 BLEU score computation to evaluate translation quality
- 🧠 Perplexity score using HuggingFace model
- 📈 API-level monitoring for request count, response time, and memory usage
- 📚 Interactive API docs via Swagger (`/docs`) and ReDoc (`/redoc`)

---

## 🗂 Project Structure

+------------+        POST /translate        +------------------------+
|            | ---------------------------> |                        |
|  USER/DEV  |                              |  FastAPI Translation    |
| (sends text)                              |        Server           |
|            | <--------------------------- |                        |
+------------+         JSON Response         +------------------------+
                                                |         |
                                   +------------+         +-------------+
                                   |                                  |
                           Google Translate                 HuggingFace M2M100
                          (Translation output)              (Reference + Perplexity)


