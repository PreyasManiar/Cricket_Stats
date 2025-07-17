# 🏏 Cricket Stats Dashboard

An interactive Streamlit dashboard that visualizes ball-by-ball cricket data to analyze batsman, bowler, team, and over-wise performance.

## 📂 Features

- 📊 Total Runs, Balls Faced, Strike Rate, Aggression Index
- 🚀 4s and 6s distribution, Dot % and Boundary %
- 🎯 Phase-wise Analysis (Powerplay, Middle, Death overs)
- 📈 Over-wise Runs, Wickets, Economical Overs
- 🧠 MVP Prediction
- 📥 Supports `.csv` and `.xlsx` file uploads

## 🚀 How to Run

1. Clone the repo:
    ```bash
    git clone https://github.com/PreyasManiar/Cricket_Stats.git
    cd Cricket_Stats
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the app:
    ```bash
    streamlit run cricket_dashboard.py
    ```

4. Upload a ball-by-ball `.csv` or `.xlsx` file to begin exploring.

## 📁 Sample Dataset Format

| Balls | Batsman | Bowler | Runs | Outcome | Total Runs | Wicket | Balls Faced |
|-------|---------|--------|------|---------|-------------|--------|-------------|
| 1.1   | Rohit Sharma (C) | Bumrah | 4 | Boundary | 4 | 0 | 1 |

## 📊 Technologies

- Python
- Pandas
- Streamlit
- Matplotlib

---

## 📬 Contact

Made with ❤️ by [Preyas Maniar](https://github.com/PreyasManiar)
