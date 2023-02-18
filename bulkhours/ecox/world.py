def get_mapgeneric(df):
    import geopandas as gpd

    world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

    world = world[(world.pop_est > 0) & (world.name != "Antarctica")]
    # world[world.continent == 'South America']
    return world.merge(df, how="left", left_on="name", right_index=True)


def geo_format(df, timeopt):
    from ..core import data

    cont = data.get_core_data("continent.tsv").drop(columns=["continent"])
    df = df.merge(cont, how="left", on="country")

    df["country"] = df["country"].str.replace("United States", "United States of America")
    df["country"] = df["country"].str.replace("Democratic Republic of Congo", "Dem. Rep. Congo")

    if type(timeopt) == int:
        df = df[df["year"] <= timeopt]
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
    return get_mapgeneric(get_poverty(**kwargs).set_index("country"))


def get_gdp(credit=True, timeopt=None, **kwargs):
    from ..core import data

    df = data.get_core_data(
        "world_gdp_hist", drop=["Country Code", "Indicator Name", "Indicator Code", "Unnamed: 66"], credit=credit
    )
    df = df.set_index("Country Name").stack().to_frame().reset_index()
    df.columns = ["country", "year", "gdp"]

    return geo_format(df, timeopt)


def get_mapgdp(**kwargs):
    return get_mapgeneric(get_gdp(**kwargs).set_index("country"))


def get_macro(credit=True, **kwargs):
    from ..core import data

    return data.get_core_data("countries", credit=credit)


def get_mapmacro(**kwargs):
    return get_mapgeneric(get_macro(**kwargs))


def plotCountryPatch(world, axes, country_name, fcolor):
    # then plot some countries on top
    # plotCountryPatch(world, ax2, 'Namibia', 'red')
    # plotCountryPatch(world, ax2, 'Libya', 'green')

    # plot a country on the provided axes
    from descartes import PolygonPatch

    nami = world[world.name == country_name]
    namigm = nami.__geo_interface__["features"]  # geopandas's geo_interface
    namig0 = {"type": namigm[0]["geometry"]["type"], "coordinates": namigm[0]["geometry"]["coordinates"]}
    axes.add_patch(PolygonPatch(namig0, fc=fcolor, ec="black", alpha=0.85, zorder=2))