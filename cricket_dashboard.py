import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("\U0001F3CF Cricket Match Dashboard")

# Upload CSV or Excel file
file = st.file_uploader("Upload your cricket match file (CSV or Excel)", type=["csv", "xlsx"])

if file:
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    df.columns = df.columns.str.strip()
    df.rename(columns={' ': 'Balls'}, inplace=True)

    if 'Balls' not in df.columns or 'Outcome' not in df.columns:
        st.error("Required columns 'Balls' or 'Outcome' not found. Please check your data.")
    else:
        df['Over'] = df['Balls'].astype(str).str.split('.').str[0].astype(int)
        df['Phase'] = pd.cut(df['Over'], bins=[0, 6, 15, 20], labels=['Powerplay', 'Middle', 'Death'])
        legal_df = df[df['Outcome'] != 'Wide Ball']

        st.sidebar.title("\U0001F4CA Graph Options")
        graph_options = st.sidebar.multiselect("Choose Graphs to Display", [
            "Total Runs by Batsman",
            "Balls Faced by Batsman",
            "Strike Rate by Batsman",
            "Aggression Index",
            "Number of 4s and 6s",
            "Boundary Percentage",
            "Dot Ball Percentage",
            "Dismissals (Wickets per Batsman)",
            "Runs per Phase",
            "Strike Rate per Phase",
            "Dot Balls or Wickets per Phase",
            "Powerplay vs Death Over Comparison",
            "Runs per Over",
            "Wickets per Over",
            "Most Economical Over",
            "Balls Played per Over",
            "Runs per Bowler",
            "Wickets per Bowler",
            "Economy per Bowler",
            "Dot Ball % per Bowler",
            "Total Team Score",
            "Extras Count",
            "Total Balls, Boundaries, Wickets",
            "Run Rate per Over",
            "Top Run Scorers (Bar Chart)",
            "Runs per Over (Line Chart)",
            "Outcome Pie Chart (for a Batsman)",
            "Boundary Hitters (Horizontal Bar)",
            "Phase-wise Stacked Bar Chart",
            "MVP of the Match"
        ])

        for graph_option in graph_options:
            st.subheader(graph_option)

            if graph_option == "Total Runs by Batsman":
                runs = legal_df.groupby('Batsman')['Runs'].sum()
                st.bar_chart(runs)

            elif graph_option == "Balls Faced by Batsman":
                balls = legal_df.groupby('Batsman').size()
                st.bar_chart(balls)

            elif graph_option == "Strike Rate by Batsman":
                runs = legal_df.groupby('Batsman')['Runs'].sum()
                balls = legal_df.groupby('Batsman').size()
                sr = (runs / balls * 100).round(2)
                st.bar_chart(sr)

            elif graph_option == "Aggression Index":
                runs = legal_df.groupby('Batsman')['Runs'].sum()
                balls = legal_df.groupby('Batsman').size()
                fours = legal_df[legal_df['Runs'] == 4].groupby('Batsman').size()
                sixes = legal_df[legal_df['Runs'] == 6].groupby('Batsman').size()
                boundary_percent = ((fours + sixes) / balls * 100).fillna(0)
                strike_rate = (runs / balls * 100).fillna(0)
                aggression_index = (strike_rate * boundary_percent / 100).round(2)
                st.bar_chart(aggression_index)

            elif graph_option == "Number of 4s and 6s":
                fours = legal_df[legal_df['Runs'] == 4].groupby('Batsman').size()
                sixes = legal_df[legal_df['Runs'] == 6].groupby('Batsman').size()
                st.bar_chart(pd.DataFrame({"Fours": fours, "Sixes": sixes}).fillna(0))

            elif graph_option == "Boundary Percentage":
                fours = legal_df[legal_df['Runs'] == 4].groupby('Batsman').size()
                sixes = legal_df[legal_df['Runs'] == 6].groupby('Batsman').size()
                balls = legal_df.groupby('Batsman').size()
                bp = ((fours + sixes) / balls * 100).round(2).fillna(0)
                st.bar_chart(bp)

            elif graph_option == "Dot Ball Percentage":
                dots = legal_df[legal_df['Outcome'] == 'Dot Ball'].groupby('Batsman').size()
                balls = legal_df.groupby('Batsman').size()
                dot_pct = (dots / balls * 100).fillna(0)
                st.bar_chart(dot_pct)

            elif graph_option == "Dismissals (Wickets per Batsman)":
                wkts = df[df['Wicket'] == 1].groupby('Batsman').size()
                st.bar_chart(wkts)

            elif graph_option == "Runs per Phase":
                phase_runs = df.groupby('Phase')['Runs'].sum()
                st.bar_chart(phase_runs)

            elif graph_option == "Strike Rate per Phase":
                phase_sr = legal_df.groupby(['Phase', 'Batsman'])['Runs'].sum() / legal_df.groupby(['Phase', 'Batsman']).size() * 100
                st.dataframe(phase_sr.round(2).unstack(fill_value=0))

            elif graph_option == "Dot Balls or Wickets per Phase":
                dots = df[df['Outcome'] == 'Dot Ball'].groupby('Phase').size()
                wkts = df[df['Wicket'] == 1].groupby('Phase').size()
                st.bar_chart(pd.DataFrame({"Dot Balls": dots, "Wickets": wkts}).fillna(0))

            elif graph_option == "Powerplay vs Death Over Comparison":
                pp = df[df['Phase'] == 'Powerplay']['Runs'].sum()
                death = df[df['Phase'] == 'Death']['Runs'].sum()
                st.bar_chart(pd.Series({"Powerplay": pp, "Death": death}))

            elif graph_option == "Runs per Over":
                over_runs = df.groupby('Over')['Runs'].sum()
                st.bar_chart(over_runs)

            elif graph_option == "Wickets per Over":
                over_wickets = df[df['Wicket'] == 1].groupby('Over').size()
                st.bar_chart(over_wickets)

            elif graph_option == "Most Economical Over":
                over_runs = df.groupby('Over')['Runs'].sum()
                min_runs = over_runs.min()
                economical_over = over_runs[over_runs == min_runs]
                st.write("Most Economical Over(s):")
                st.write(economical_over)

            elif graph_option == "Balls Played per Over":
                balls_over = df.groupby('Over').size()
                st.bar_chart(balls_over)

            elif graph_option == "Runs per Bowler":
                bowler_runs = df.groupby('Bowler')['Runs'].sum()
                st.bar_chart(bowler_runs)

            elif graph_option == "Wickets per Bowler":
                bowler_wkts = df[df['Wicket'] == 1].groupby('Bowler').size()
                st.bar_chart(bowler_wkts)

            elif graph_option == "Economy per Bowler":
                runs = df.groupby('Bowler')['Runs'].sum()
                overs = df.groupby('Bowler')['Over'].nunique()
                eco = (runs / overs).round(2).fillna(0)
                st.bar_chart(eco)

            elif graph_option == "Dot Ball % per Bowler":
                dots = df[df['Outcome'] == 'Dot Ball'].groupby('Bowler').size()
                balls = df.groupby('Bowler').size()
                dot_pct = (dots / balls * 100).round(2).fillna(0)
                st.bar_chart(dot_pct)

            elif graph_option == "Total Team Score":
                total_score = df['Runs'].sum()
                st.metric("Total Runs Scored", total_score)

            elif graph_option == "Extras Count":
                extras = ['Wide Ball', 'No Ball', 'Bye', 'Leg Bye']
                extras_count = df[df['Outcome'].isin(extras)]['Outcome'].value_counts()
                st.bar_chart(extras_count)

            elif graph_option == "Total Balls, Boundaries, Wickets":
                total_balls = df.shape[0]
                total_boundaries = df[df['Outcome'].isin(['Boundary', 'Six'])].shape[0]
                total_wickets = df[df['Wicket'] == 1].shape[0]
                st.metric("Balls", total_balls)
                st.metric("Boundaries", total_boundaries)
                st.metric("Wickets", total_wickets)

            elif graph_option == "Run Rate per Over":
                over_runs = df.groupby('Over')['Runs'].sum()
                run_rate = (over_runs / 6).round(2)
                st.bar_chart(run_rate)

            elif graph_option == "Top Run Scorers (Bar Chart)":
                runs = df.groupby('Batsman')['Runs'].sum().sort_values(ascending=False)
                st.bar_chart(runs)

            elif graph_option == "Runs per Over (Line Chart)":
                over_runs = df.groupby('Over')['Runs'].sum()
                fig, ax = plt.subplots()
                ax.plot(over_runs.index, over_runs.values, marker='o')
                plt.title("Runs per Over")
                st.pyplot(fig)

            elif graph_option == "Outcome Pie Chart (for a Batsman)":
                batsman = st.selectbox("Select Batsman", df['Batsman'].unique())
                outcomes = df[df['Batsman'] == batsman]['Outcome'].value_counts()
                fig, ax = plt.subplots()
                outcomes.plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax)
                plt.ylabel('')
                plt.title(f'Outcome Distribution - {batsman}')
                st.pyplot(fig)

            elif graph_option == "Boundary Hitters (Horizontal Bar)":
                boundaries = df[df['Outcome'].isin(['Boundary', 'Six'])].groupby('Batsman').size()
                fig, ax = plt.subplots()
                boundaries.sort_values().plot(kind='barh', ax=ax)
                plt.title("Top Boundary Hitters")
                st.pyplot(fig)

            elif graph_option == "Phase-wise Stacked Bar Chart":
                phase_data = df.groupby(['Phase', 'Over'])['Runs'].sum().unstack().fillna(0)
                st.bar_chart(phase_data.T)

            elif graph_option == "MVP of the Match":
                runs = legal_df.groupby('Batsman')['Runs'].sum()
                balls = legal_df.groupby('Batsman').size()
                sr = (runs / balls * 100).fillna(0)
                mvp_score = (runs + 0.5 * sr).round(2)
                mvp = pd.DataFrame({'Runs': runs, 'Balls': balls, 'SR': sr, 'Score': mvp_score}).sort_values(by='Score', ascending=False)
                st.dataframe(mvp.head(5))
                st.success(f"\U0001F3C6 MVP: {mvp.index[0]} with Score {mvp.iloc[0]['Score']}")
