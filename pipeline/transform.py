import pandas as pd
from datetime import timedelta
from typing import Dict

class Transformer:
    """
    Reads rows (list of dicts) from DB and exposes methods to compute insights.

    Methods:
        - from_records(records): build object
        - rolling_trend(window_days)
        - weekly_summary(end_date)
        - summarize_notes(n=5)
    """

    def __init__(self, records):
        self.df = pd.DataFrame(records)
        if not self.df.empty:
            self.df['date'] = pd.to_datetime(self.df['date']).dt.date
            self.df = self.df.sort_values('date')

    @classmethod
    def from_records(cls, records):
        return cls(records)

    def aggregate_basic(self) -> Dict:
        if self.df.empty:
            return {}
        return {
            'avg_mood': round(self.df['mood'].mean(), 2),
            'avg_energy': round(self.df['energy'].mean(), 2),
            'avg_stress': round(self.df['stress'].mean(), 2),
            'highest_stress_day': self.df.loc[self.df['stress'].idxmax(), 'date'],
            'lowest_energy_day': self.df.loc[self.df['energy'].idxmin(), 'date']
        }

    def weekly_summary(self, end_date=None):
        if self.df.empty:
            return {}
        if end_date is None:
            end_date = self.df['date'].max()
        start_date = end_date - timedelta(days=6)
        mask = (self.df['date'] >= start_date) & (self.df['date'] <= end_date)
        week = self.df.loc[mask]
        if week.empty:
            return {}
        return {
            'start_date': start_date,
            'end_date': end_date,
            'avg_mood': round(week['mood'].mean(), 2),
            'avg_energy': round(week['energy'].mean(), 2),
            'avg_stress': round(week['stress'].mean(), 2)
        }

    def format_weekly_summary(self, end_date=None) -> str:
        """
        Returns a clean, human-readable weekly summary as a string.
        """
        summary = self.weekly_summary(end_date)
        if not summary:
            return "No data for this week."

        lines = [
            "Weekly Summary (Most Recent)",
            f"Start Date: {summary['start_date']}",
            f"End Date:   {summary['end_date']}",
            f"Average Mood:   {summary['avg_mood']}",
            f"Average Energy: {summary['avg_energy']}",
            f"Average Stress: {summary['avg_stress']}"
        ]


        return "\n".join(lines)

    def rolling_trend(self, window_days=7):
        if self.df.empty:
            return pd.DataFrame()

        tmp = self.df.set_index(pd.to_datetime(self.df['date']))
        tmp_rolled = tmp[['mood', 'energy', 'stress']].rolling(f"{window_days}D").mean()
        tmp_rolled = tmp_rolled.dropna().reset_index()
        tmp_rolled['date'] = tmp_rolled['date'].dt.date

        return tmp_rolled[['date', 'mood', 'energy', 'stress']]

