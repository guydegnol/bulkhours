import numpy as np


def get_mapgeneric(df):
    import geopandas as gpd

    if "continent" in df.columns:
        del df["continent"]

    world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

    world = world[(world.pop_est > 0) & (world.name != "Antarctica")]
    # world[world.continent == 'South America']
    return world.merge(df.set_index("country"), how="left", left_on="name", right_index=True)


def geo_format(df, timeopt):
    from ..core import data

    cont = data.get_core_data("continent.tsv")
    df = df.merge(cont, how="left", on="country")

    df["country"] = df["country"].str.replace("United States", "United States of America")
    df["country"] = df["country"].str.replace("Democratic Republic of Congo", "Dem. Rep. Congo")

    if type(timeopt) == int:
        df = df[df["year"] <= timeopt]
    if timeopt == "first":
        df = df[df.groupby("country")["year"].rank(method="dense", ascending=True) == 1.0]
    if timeopt == "last" or type(timeopt) == int:
        df = df[df.groupby("country")["year"].rank(method="dense", ascending=False) == 1.0]
    if timeopt:
        df = df.groupby(["country", "year"]).mean().reset_index()

    return df


def get_poverty(credit=True, timeopt=None, **kwargs):
    from ..core import data

    df = data.get_core_data("poverty", credit=credit)
    return geo_format(df, timeopt)


def get_mappoverty(**kwargs):
    return get_mapgeneric(get_poverty(**kwargs))


def get_gdp(credit=True, timeopt=None, **kwargs):
    from ..core import data

    df = data.get_core_data(
        "world_gdp_hist", drop=["Country Code", "Indicator Name", "Indicator Code", "Unnamed: 66"], credit=credit
    )
    df = df.set_index("Country Name").stack().to_frame().reset_index()
    df.columns = ["country", "year", "gdp"]

    return geo_format(df, timeopt)


def get_mapgdp(**kwargs):
    return get_mapgeneric(get_gdp(**kwargs))


def get_macro(credit=True, **kwargs):
    from ..core import data

    df = data.get_core_data("macro", credit=credit)
    return geo_format(df, None)


def get_corruption(credit=True, show_truth=False, **kwargs):
    from ..core import data

    df = data.get_core_data("macro", credit=credit)

    if not show_truth:
        df["corruption_index"] = df["corruption_index"].where(
            ~df.index.isin(["Spain", "Japan", "Sweden", "Romania"]), other=np.nan
        )
    macro = df[["annual_income", "corruption_index", "gdp_per_capita", "unemployment_rate"]]
    macro = macro.dropna(subset=["annual_income", "gdp_per_capita", "unemployment_rate"])

    return geo_format(macro, None)


def get_mapmacro(**kwargs):
    return get_mapgeneric(get_macro(**kwargs))
