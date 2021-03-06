import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline

def heaviside_step(x):
    return np.heaviside([x], 0)[0]

def pl_harvest(init_pl, sr, partial_rate):
    """
    init_pl: initial of PL 
    sr: survival rate
    partial_rate: partial harvest rate in each harvesting
    """
    return init_pl*sr*partial_rate

def body_weight(wn, w0, alpha, t0, t, hx=1):
    """
    wn: shrimp max weight g
    w0: shrimp stocking weight (initial weight)
    alpha: shrimp growth rate
    t0: initial time
    t: time
    hx: constant derive function. default 1.
    """
    wt = wn**(1/3) - (wn**(1/3) - w0**(1/3)) * np.exp(-alpha*(hx*t - hx*t0))
    return wt**3

def count_biomassa(w, t, sr=0.8):
    """
    w: weight ke-t
    t: jumlah tebar
    sr: survival rate
    """
    b = w * t * sr
    return b

def size_count(w):
    """
    w: weight ke-t
    """
    return 1000/w

def realize_counter(a: float, w: int, p: float):
    """
    a: persentase panen
    w: weight ke n
    p: price 
    """
    return a*w*p

def price_function(path, sep=";", col_size="size_count", col_price="price"):
    """
    path: path file for the price's data
    sep: delimiter/separator for the csv file
    col_size: columns name for size count of shrimp
    col_price: columns name for price of shrimp
    """
    df = pd.read_csv(path, sep=sep)
    x_sample = df[col_size].tolist()[::-1]
    y_sample = df[col_price].tolist()[::-1]
    f = CubicSpline(x_sample, y_sample, bc_type="natural")
    return f

def biomass_harvest(data, docpartial1, docpartial2, docpartial3):
    """
    data: biomassa data
    docpartial1: docpartial1
    docpartial2: docpartial2
    docpartial3: docpartial3
    """
    b1 = data[docpartial1] - data[docpartial1+1]
    b2 = data[docpartial2] - data[docpartial2+1]
    b3 = data[docpartial3] - data[docpartial3+1]
    return b1, b2, b3, data[-1]

def feed_formula3(path, sep=";", colname="Formula 3"):
    df = pd.read_csv(path, sep=sep)
    return df[colname].tolist()