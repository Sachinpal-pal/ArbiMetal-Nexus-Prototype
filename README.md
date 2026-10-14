ArbiMetal Nexus 

* AI-powered Statistical Arbitrage Dashboard for global and hyper-local commodity markets.

ArbiMetal Nexus is a premium SaaS-style platform designed to bridge the gap between global commodity prices (Wall Street) and local retail markets. It provides real-time pricing, AI-driven market insights, and hyper-local geographical price adjustments for major commodities.

# Key Features

* Hyper-Local Geo-Pricing Engine: Calculates precise local prices by dynamically fetching global COMEX/NYMEX futures and live Forex rates, adjusting for local taxes and state-level premiums (e.g., specific Indian states, Dubai, Europe).
* AI Market Analyst: An intelligent summarizer that analyzes near-term vs. long-term moving averages to provide simple, actionable advice (Shortage/Wait vs. Undervalued/Buy).
* Interactive 1-Year Price Trend: High-quality, interactive Plotly charts comparing live closing prices with 60-day historical averages to easily visualize market heat.
* Virtual AI Analyst Chatbot: An integrated smart assistant that answers user queries (e.g., "Should I buy today?") based on real-time market indicators.
* Multi-language Support: Dynamic UI translation supporting English, Hindi, and Spanish for diverse user accessibility.
* Date Time-Machine: Allows users to deep-dive into exact local pricing, opening/closing rates, and highs/lows for any specific past date within the last year.

# Tech Stack

* Language: Python
* Frontend/Framework: Streamlit (with Custom CSS/Glassmorphism UI)
* Data Sourcing: `yfinance` (Real-time Yahoo Finance API for Commodities & Forex)
* Data Visualization: Plotly (`plotly.graph_objects`)
* Data Manipulation: Pandas
* Localization: `googletrans`

---
*Built for Hackathon Prototype Submission*
