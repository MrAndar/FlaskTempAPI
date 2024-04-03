from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)
stations_df = pd.read_csv("small_data/stations.txt", skiprows=17)
stations = stations_df[["STAID", "STANAME                                 "]]


@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())


@app.route("/api/v1/<station>/<date>/")
def temperatures(station, date):
    try:
        filename = "small_data/TG_STAID" + str(station).zfill(6) + ".txt"
        df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
        temp = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10
        try:
            float(temp)
        except TypeError:
            temp = "No data for this date"
    except FileNotFoundError:
        station = "Station does not exist"
        temp = "No data"

    return {"station ID": station, "date": date, "temperature": temp}


@app.route("/api/v1/<station>/")
def all_data(station):
    filename = "small_data/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    result = df.to_dict(orient="records")
    return result


@app.route("/api/v1/year/<station>/<year>/")
def year_data(station, year):
    filename = "small_data/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")
    return result


if __name__ == "__main__":
    app.run(debug=True)
