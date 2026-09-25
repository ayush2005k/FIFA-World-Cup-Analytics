# ⚽ FIFA World Cup Analytics

A complete end-to-end Sports Analytics and Data Engineering project built around the FIFA World Cup.

## Project Overview

This project collects, cleans, stores, and analyzes FIFA World Cup data from multiple sources to create an analytics platform using Python, SQL, and Power BI.

The project demonstrates:

- ETL Pipelines
- Data Cleaning
- Data Validation
- Database Design
- SQL Analytics
- Sports Analytics
- Interactive Dashboards

---

## Tech Stack

- Python
- Pandas
- Requests
- BeautifulSoup
- MySQL
- Power BI
- Git & GitHub

---

## Data Sources

### Wikipedia
- Stadiums
- Qualified Teams
- Group Standings
- Match Schedule
- Knockout Bracket

### FIFA
- FIFA Rankings
- Confederations
- Country Codes
- World Cup History

### FBref
- Team Statistics
- Shooting
- Passing
- Possession
- Defensive Actions
- Goalkeeping

### StatsBomb
- Matches
- Events
- Lineups
- Competitions

---

## Project Structure

```text
FIFA-World-Cup-Analytics/
│
├── data/
│   ├── raw/
│   │   ├── wikipedia/
│   │   ├── fifa/
│   │   ├── fbref/
│   │   ├── statsbomb/
│   │   └── manual/
│   │
│   └── processed/
│
├── scripts/
│   ├── scraping/
│   ├── cleaning/
│   ├── validation/
│   └── analytics/
│
├── database/
├── sql/
├── dashboard/
├── reports/
└── notebooks/
```

---

## ETL Pipeline

```
Extract
    ↓
Wikipedia
FIFA
FBref
StatsBomb
    ↓
Raw CSV
    ↓
Cleaning
    ↓
Validation
    ↓
Processed CSV
    ↓
MySQL
    ↓
SQL Analysis
    ↓
Power BI Dashboard
```

---

## Current Progress

- [x] Project Structure
- [x] Wikipedia Data Collection
- [x] FIFA Reference Data
- [x] ETL for Wikipedia
- [ ] FBref Team Statistics
- [ ] FBref Player Statistics
- [ ] StatsBomb Data
- [ ] MySQL Database
- [ ] SQL Analytics
- [ ] Power BI Dashboard
- [ ] Machine Learning

---

## Future Enhancements

- Match Prediction
- Team Strength Modeling
- xG Analytics
- Interactive Dashboards
- Performance Analysis
- ELO Rating System

---

## Author

Ayush Singh
