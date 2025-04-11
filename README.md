# 🌍 Global Humanitarian Dashboard

An interactive web dashboard that visualizes and analyzes global humanitarian issues including **modern slavery**, **migration patterns**, and **refugee statistics**—designed to inform, engage, and drive awareness.

---

## 🚀 Key Features

### 📌 Modern Slavery Analysis
- Interactive world map showing slavery prevalence by country
- Regional breakdown and statistics
- Top countries with highest modern slavery rates

### 🌐 Migration Insights
- Net migration trends visualized over time
- Analysis of population vs. migration relationships
- Country-wise migration patterns

### 🏠 Refugee Statistics
- Trends in global refugee movements
- Interactive maps for refugee distribution
- Highlighting top refugee-hosting nations

---

## 🧠 Script Overview

| Script File | Description |
|-------------|-------------|
| `Global_slavery_index.py` | Loads and visualizes modern slavery data globally |
| `Refugee_Analysis.py` | Analyzes and displays trends in refugee data |
| `Migration_World_Bank_Report.py` | Explores global migration trends from World Bank data |

---

## ⚙️ Getting Started

Follow these simple steps to run the dashboard locally:

### 1. Set up a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install required dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the app
```bash
python app.py
```

### 4. View it in your browser
Open [http://localhost:5000](http://localhost:5000) in your browser to interact with the dashboard.

---

## 📊 Data Sources

- [Global Slavery Index 2023](https://www.walkfree.org/global-slavery-index/)
- [World Bank Migration Data](https://data.worldbank.org/indicator)
- [UNHCR Refugee Statistics](https://www.unhcr.org/statistics/)

---

## 🛠️ Tech Stack

- **Backend**: Flask, Dash
- **Data Analysis & Visualization**: Pandas, Plotly
- **Frontend**: Bootstrap, Custom CSS

---

## 📁 Project Structure

```
├── app.py                      # Main dashboard app
├── requirements.txt            # Python dependencies
├── static/
│   └── css/
│       └── style.css           # Custom styles
└── data/
    ├── Global_Slavery_Index_2023.csv
    ├── pop_and_net_migration.csv
    └── United_Nations_Refugee_Data.csv
```

---

## 🤝 Contributing

Have suggestions, spotted bugs, or want to contribute new features?  
You're welcome! Please open an [issue](https://github.com/your-repo/issues) or submit a pull request.
