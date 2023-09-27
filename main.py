import pandas as pd
import matplotlib as mp
from matplotlib import pyplot as plt
import zipfile
from datetime import timedelta

ARCHIVE_PATH = "data/archive.zip"
DESTINATION_PATH = "data/"
def un_zipper(zip_path: str, dest_path: str):

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Extract all the contents of the zip file to the specified directory
        zip_ref.extractall(dest_path)

# un_zipper(ARCHIVE_PATH, DESTINATION_PATH)
def plot_line(x, y):
    plt.plot(x,y)
    plt.show()

def str_to_timedelta(s):
    days, hours, minutes, seconds = map(int, s.replace(' days ', ':').split(':'))
    return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

# 0 days 00:00:00
# 0:00:00:00
# [0,00,00,00]

df = pd.read_csv("data/labels.csv")
period_a = df[df['period'] == 'train_a']
period_b = df[df['period'] == 'train_b']
period_c = df[df['period'] == 'train_c']

solar_wind = pd.read_csv("data/solar_wind.csv")
solar_wind_pd_a = solar_wind[solar_wind['period'] == 'train_a']

str_to_timedelta("0 days 00:00:00")

plt.plot(period_a["timedelta"][:100], period_a["dst"][:100],
         solar_wind_pd_a["timedelta"][:100], solar_wind_pd_a["density"][:100])
plt.show()