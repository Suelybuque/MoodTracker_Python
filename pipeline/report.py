from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from pipeline.transform import Transformer
from datetime import datetime
import os

class ReportGenerator :
    """
    Usage: rg= ReportGenerator(output_path="reports/week_2025-11-23.pdf")
    rg.create_weekly_report (summary_dict, trend_df)
    """

    def __init__(self,output_path="reports/weekly_report.pdf" ):
        self.output_path= output_path
        os.makedirs(os.path.dirname(output_path), exist_ok= True)

    def create_weekly_report(self, summary: dict, trend_df=None):
        c= canvas.Canvas(self.output_path, pagesize= letter)
        width, height = letter

        #Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(1*inch, height - 1*inch, "Mood & Energy Weekly Report")

        #Date range
        c.setFont("Helvetica", 10)
        c.drawString(1*inch, height - 1.25*inch, f"Week: {
         summary.get('start_date')} to {summary.get('end_date')}")

        #Key Metrics
        c.setFont("Helvetica-Bold", 12)
        c.drawString(1*inch, height - 1.6*inch, "Key Metrics")
        c.setFont("Helvetica", 11)
        metrics_y = height- 1.85*inch
        c.drawString(1*inch, metrics_y, f"Average mood:{summary.get('avg_mood')}")
        c.drawString(3.2*inch, metrics_y, f"Average energy:  {summary.get('avg_energy')}")
        c.drawString(1*inch, metrics_y - 0.2*inch, f"Average stress: {summary.get('avg_stress')}")

        #Notes
        c.setFont("Helvetica-Bold", 12)
        c.drawString(1 * inch, metrics_y - 0.6 * inch, "Notes (recent)")
        c.setFont("Helvetica", 10)
        notes = summary.get('top_notes', [])
        y = metrics_y - 0.8 * inch
        for note in notes[:6]:
            c.drawString(1 * inch, y, f"- {note}")
        y -= 0.18 * inch
        if y < 1 * inch:
            c.showPage()
        y = height - 1 * inch

        #Simple trend chart using matplotlib saved as png
        if trend_df is not None and not trend_df.empty:
            import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(6, 2))
        ax.plot(trend_df['date'], trend_df['mood'], label='mood')
        ax.plot(trend_df['date'], trend_df['energy'], label='energy')
        ax.plot(trend_df['date'], trend_df['stress'], label='stress')
        ax.set_title('Rolling trend')
        ax.legend()
        plt.xticks(rotation=20)
        tmp_img = self.output_path.replace('.pdf', '.png')
        fig.tight_layout()
        fig.savefig(tmp_img)
        plt.close(fig)
        c.showPage()
        c.drawImage(tmp_img, inch, height - 4 * inch, width=6 * inch,
                    preserveAspectRatio=True)
        try:
            os.remove(tmp_img)
        except Exception:
            pass
        c.save()
        return self.output_path