from pandas import Series 

def quantile1(x: Series):
    return x.quantile(0.25)

def median(x: Series):
    return x.quantile(0.50)

def quantile3(x: Series):
    return x.quantile(0.75)