# Company News Sentiment Analysis API

A FastAPI-based backend system that fetches real-time company news and performs sentiment analysis using NLP (FinBERT). The application is fully containerized using Docker.

---

## Features

- Fetch real-time company news using GNews API
- Perform sentiment analysis using FinBERT (Hugging Face)
- Extract keywords and summaries from news articles
- REST API built with FastAPI
- Dockerized for easy deployment

---

## Tech Stack

- **Backend:** FastAPI (Python), Uvicorn
- **NLP Model:** FinBERT (Hugging Face Transformers)
- **Data Source:** GNews API
- **HTTP Client:** Requests
- **Containerization:** Docker
- **Data Processing:** Python (JSON, text preprocessing)


---

## Run the Project

### 1. Clone repo
```bash
git clone https://github.com/Pratyush-0705/company-news-sentiment-api.git
cd company-news-sentiment-api
```

### 2. Create environment variables

Create a `.env` file in the root directory.

You can refer to the `.env.example` file provided in this repository for the required format.

To get your API key:
- Visit https://gnews.io/
- Sign up and generate your free API key
- Add the key to your `.env` file

Example:

```bash id="envkey1"
GNEWS_API_KEY=your_api_key_here
```

### 3. Build Docker Image
```bash
docker build -t company-news-api .
```

### 4. Run the application
```bash
docker run -p 8000:8000 --env-file .env company-news-api
```

## Sample Responses

See `/sample_responses` for example API outputs.
