# 📈 SkinCalc – CS2 Arbitrage Dashboard
 
SkinCalc is a full-stack analytical tool designed to monitor and identify price arbitrage opportunities between the **Steam Community Market** and **Skinport**. The application provides real time price comparisons for Counter-Strike 2 items, automatically calculating profit margins (**Ratio**) after accounting for platform fees and currency fluctuations.
 
---
 
## 🚀 Key Features
 
- **Real time Price Tracking** - Fetches the lowest sell orders and highest buy orders directly from Steam's infrastructure.
- **API Reverse Engineering** - Bypasses slow HTML scraping by utilizing Steam's internal JSON endpoints (`itemordershistogram`), ensuring faster data acquisition and high resilience against UI changes.
- **Arbitrage Calculator** - Automated "Ratio" calculation factoring in Skinport's tiered sales commissions.
- **Hybrid Data Sourcing** - Synchronizes official Skinport API data with a custom-built asynchronous Steam scraper.
 
---
 
## 🛠️ Technical Stack
 
### Backend
| Technology | Role |
|---|---|
| **Python (FastAPI)** | Asynchronous API handling for high-concurrency data fetching |
| **SQLAlchemy ORM** | Database management with relational mapping between items, markets, and historical prices |
| **Httpx & BeautifulSoup4** | Asynchronous HTTP client and HTML parsing for robust web scraping |
| **Uvicorn** | High-performance ASGI server implementation |
 
### Frontend
| Technology | Role |
|---|---|
| **Next.js 14 / React** | Modern framework utilizing the `App Router` for optimized routing and rendering |
| **TypeScript** | Full-scale static typing for enhanced code reliability and maintainability |
| **Tailwind CSS** | Responsive, utility-first styling with a custom "Deep Ocean & Red Velvet" dark-mode palette |
 
---
 
## ⚙️ Setup & Installation
 

### 1. Backend setup
 
```bash
cd backend
pip install -e .
uvicorn main:app --reload
```
 
### 2. Frontend setup
 
```bash
cd frontend
npm install
npm run dev
```