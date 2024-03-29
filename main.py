import numpy as np
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

#un_zipper(ARCHIVE_PATH, DESTINATION_PATH)
#
def plot_line(x, y):
    plt.plot(x,y)
    plt.show()

def str_to_timedelta(s):
    days, hours, minutes, seconds = map(int, s.replace(' days ', ':').split(':'))
    return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

# 0 days 00:00:00
# 0:00:00:00
# [0,00,00,00]

def two_dimention_timeplot():

    df = pd.read_csv("data/labels.csv")
    period_a = df[df['period'] == 'train_a']
    period_b = df[df['period'] == 'train_b']
    period_c = df[df['period'] == 'train_c']

    solar_wind = pd.read_csv("data/solar_wind.csv")
    solar_wind_pd_a = solar_wind[solar_wind['period'] == 'train_a']

    str_to_timedelta("0 days 00:00:00")

    #period_a["timedelta"][:100].map(str_to_timedelta), period_a["dst"][:100],
    plt.plot(period_a["timedelta"][:100].map(str_to_timedelta), period_a["dst"][:100], solar_wind_pd_a["timedelta"][:6000].map(str_to_timedelta), solar_wind_pd_a["density"][:6000])
def function_for_plotting_the_satellite_position():
    #Create 3D plot of satellite positional data
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    satellite_pos = pd.read_csv("data/satellite_pos.csv")
    period_a_sp = satellite_pos[satellite_pos['period'] == 'train_a']
    period_b_sp = satellite_pos[satellite_pos['period'] == 'train_b']
    period_c_sp = satellite_pos[satellite_pos['period'] == 'train_c']
    size = -1
    gse_x = period_b_sp["gse_x_ace"][0:size]
    gse_y = period_b_sp["gse_y_ace"][0:size]
    gse_z = period_b_sp["gse_z_ace"][0:size]
    ax.scatter(gse_x, gse_y, gse_z)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    #min = pd.concat([gse_x, gse_y, gse_z]).min()
    #max = pd.concat([gse_x, gse_y, gse_z]).max()
    #ax.set_xlim3d(min, max)
    #ax.set_ylim3d(min, max)
    #ax.set_zlim3d(min, max)
    #ax.set_aspect('equal', adjustable='box')
    #ax.view_init(elev=30, azim=45)
    #gse_x_median = gse_x.median()
    #gse_y_median = gse_y.median()
    #gse_z_median = gse_z.median()
    plt.show()

def lots_of_mag_vectors_across_time():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    rowskip = 3600
    solar_data = pd.read_csv("data/solar_wind.csv")
    solar_data = solar_data.iloc[rowskip:]
    period_a_sp = solar_data[solar_data['period'] == 'train_a']
    period_b_sp = solar_data[solar_data['period'] == 'train_b']
    period_c_sp = solar_data[solar_data['period'] == 'train_c']
    size = 1000
    gse_x = [x for n, x in enumerate(period_b_sp["bx_gse"]) if n % rowskip == 0]
    gse_y = [x for n, x in enumerate(period_b_sp["by_gse"]) if n % rowskip == 0]
    gse_z = [x for n, x in enumerate(period_b_sp["bz_gse"]) if n % rowskip == 0]
    ax.scatter(gse_x, gse_y, gse_z)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    plt.show()


solar_data = pd.read_csv("data/solar_wind.csv")

period_a = solar_data[solar_data['period'] == 'train_a']
data_length = 1700

def normalizer(df):
    df_max = df.max()
    df_min = df.min()
    return (df - df_min) / (df_max - df_min)

def movingAvg(data, windowSize):
    ferret = []

    for i in range(len(data)):
        fish = sum(data[i:i+windowSize])/windowSize
        ferret.append(fish)
    return ferret


def removeNan(data):
    for i in range(len(data)):
        if (np.isnan(data[i])):
            notNanIndexForward = 0
            notNanIndexBackward = 0
            while (np.isnan(data[i+notNanIndexForward]) and (i+notNanIndexForward) != len(data) - 1):
                notNanIndexForward += 1
            while (np.isnan(data[i-notNanIndexBackward]) and (i-notNanIndexBackward) != 0):
                notNanIndexBackward += 1
            if ((i-notNanIndexBackward) == 0):
                data[i] = data[i+notNanIndexForward]
            elif ((i+notNanIndexForward) == len(data) - 1):
                data[i] = data[i-notNanIndexBackward]
            else:
                data[i] = (data[i+notNanIndexForward] + data[i-notNanIndexBackward])/2
    return data

data = normalizer(period_a["temperature"][:data_length])
bob = [float("nan"), 1, 23, float("nan"), float("nan"), 43, float("nan")]
lizard = removeNan(data)
twoDogs = movingAvg(lizard, 10)


# period_a["timedelta"][:data_length].map(str_to_timedelta), data,
# period_a["timedelta"][:data_length].map(str_to_timedelta), lizard

plt.plot(period_a["timedelta"][:data_length].map(str_to_timedelta), movingAvg(lizard, 100))

plt.show()