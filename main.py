

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    from alpha_vantage.timeseries import TimeSeries
    load_dotenv()
    ts = TimeSeries(key=os.environ.get("ALPHA_VANTAGE_KEY"), output_format="pandas")
    df = ts.get_symbol_search("soja") #SOJA3.SAO
    print(df)