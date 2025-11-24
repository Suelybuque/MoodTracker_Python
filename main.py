import click
from pipeline.extract import collect_and_store, seed_demo_data
from pipeline.db import MoodDB
from pipeline.load import upload_to_s3, upload_to_gcs
from pipeline.transform import Transformer
from pipeline.report import ReportGenerator
from datetime import date

@click.group()
def cli():
    pass

@cli.command()
@click.option('--mood', required= True, type= int)
@click.option('--energy', required= True, type= int)
@click.option('--stress', required= True, type= int)
@click.option('--notes', default='')

def add(mood, energy, stress, notes):
    collect_and_store(mood, energy, stress ,notes)
    print('Saved check-in')

@cli.command()
def seed():
    seed_demo_data(21)
    print('Seeded demo deta')

@cli.command()
def report():
    db= MoodDB()
    records= db.fetch_all()
    t= Transformer.from_records(records)
    summary= t.weekly_summary()
    trend= t.rolling_trend(7)
    rg= ReportGenerator(output_path=f"reports/weekly_{summary.get('end_date')}.pdf")
    out= rg.create_weekly_report(summary, trend)
   # upload_to_s3(out, "my-mood-bucket")
    #upload_to_gcs(out, "my-mood-bucket-gcs")
    print('Report ready:', out)

if __name__== '__main__':
    cli()