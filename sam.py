
import streamlit as st
import requests
import pymysql
import pandas as pd


# ---------------------------------------------------
# STREAMLIT PAGE
# ---------------------------------------------------

st.set_page_config(
    page_title="Earthquake Data",
    page_icon="🌍",
    layout="wide"
)

st.title("streamlit + mysql + usgs API")


# ---------------------------------------------------
# SIDEBAR - DATE SELECTION
# ---------------------------------------------------

st.sidebar.header("Earthquake Search")

startdate = st.sidebar.date_input(
    "Start Date",
    value=pd.to_datetime("2020-01-01")
)

enddate = st.sidebar.date_input(
    "End Date",
    value=pd.to_datetime("2020-02-01")
)


# ---------------------------------------------------
# MYSQL CONNECTION
# ---------------------------------------------------

def get_connection():

    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="sammathew@12345",
        port=3306
    )

    return connection


# ---------------------------------------------------
# FETCH DATA FROM USGS
# ---------------------------------------------------

def get_earthquake_data(startdate, enddate):

    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

    params = {
        "format": "geojson",
        "starttime": str(startdate),
        "endtime": str(enddate)
    }

    response = requests.get(url, params=params)

    response.raise_for_status()

    return response.json()


# ---------------------------------------------------
# CONVERT API DATA INTO RECORDS
# ---------------------------------------------------

def create_records(data):

    records = []

    for earthquake in data["features"]:

        properties = earthquake["properties"]
        coordinates = earthquake["geometry"]["coordinates"]

        records.append({
            "id": earthquake["id"],
            "time": properties["time"],
            "updated": properties["updated"],
            "latitude": coordinates[1],
            "longitude": coordinates[0],
            "depth_km": coordinates[2],
            "mag": properties["mag"],
            "magType": properties["magType"],
            "place": properties["place"],
            "status": properties["status"],
            "tsunami": properties["tsunami"],
            "alert": properties["alert"],
            "felt": properties["felt"],
            "cdi": properties["cdi"],
            "mmi": properties["mmi"],
            "sig": properties["sig"],
            "net": properties["net"],
            "code": properties["code"],
            "ids": properties["ids"],
            "sources": properties["sources"],
            "types": properties["types"],
            "nst": properties["nst"],
            "dmin": properties["dmin"],
            "rms": properties["rms"],
            "gap": properties["gap"],
            "type": properties["type"],
            
        })

    return records


# ---------------------------------------------------
# CREATE DATABASE
# ---------------------------------------------------

def create_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "CREATE DATABASE IF NOT EXISTS earthquake_db"
    )

    connection.commit()

    cursor.close()
    connection.close()


# ---------------------------------------------------
# CREATE TABLE
# ---------------------------------------------------

def create_table():

    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="sammathew@12345",
        port=3306,
        database="earthquake_db"
    )

    cursor = connection.cursor()

    CREATE_QUERY = """
    CREATE TABLE IF NOT EXISTS earthquakes (

        id VARCHAR(50),
        time BIGINT,
        updated BIGINT,
        latitude FLOAT,
        longitude FLOAT,
        depth_km FLOAT,
        mag FLOAT,
        magType VARCHAR(20),
        place VARCHAR(255),
        status VARCHAR(20),
        tsunami INT,
        alert VARCHAR(20),
        felt INT,
        cdi FLOAT,
        mmi FLOAT,
        sig INT,
        net VARCHAR(20),
        code VARCHAR(50),
        ids TEXT,
        sources TEXT,
        types TEXT,
        nst INT,
        dmin FLOAT,
        rms FLOAT,
        gap FLOAT,
        type VARCHAR(50)
    )
    """

    cursor.execute(CREATE_QUERY)

    connection.commit()

    cursor.close()
    connection.close()


# ---------------------------------------------------
# INSERT DATA
# ---------------------------------------------------

def insert_data(records):

    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="sammathew@12345",
        port=3306,
        database="earthquake_db"
    )

    cursor = connection.cursor()

    INSERT_QUERY = """
    INSERT INTO earthquakes
    (
        id,
        time,
        updated,
        latitude,
        longitude,
        depth_km,
        mag,
        magType,
        place,
        status,
        tsunami,
        alert,
        felt,
        cdi,
        mmi,
        sig,
        net,
        code,
        ids,
        sources,
        types,
        nst,
        dmin,
        rms,
        gap,
        type
    )
    VALUES (
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s
    )
    """

    insertion_list = []

    for dic in records:

        values = (
            dic["id"],
            dic["time"],
            dic["updated"],
            dic["latitude"],
            dic["longitude"],
            dic["depth_km"],
            dic["mag"],
            dic["magType"],
            dic["place"],
            dic["status"],
            dic["tsunami"],
            dic["alert"],
            dic["felt"],
            dic["cdi"],
            dic["mmi"],
            dic["sig"],
            dic["net"],
            dic["code"],
            dic["ids"],
            dic["sources"],
            dic["types"],
            dic["nst"],
            dic["dmin"],
            dic["rms"],
            dic["gap"],
            dic["type"]
            
        )

        insertion_list.append(values)

    cursor.executemany(
        INSERT_QUERY,
        insertion_list
    )

    connection.commit()

    cursor.close()
    connection.close()

    return len(insertion_list)


# ---------------------------------------------------
# GET DATA FROM MYSQL
# ---------------------------------------------------

def get_database_data():

    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="sammathew@12345",
        port=3306,
        database="earthquake_db"
    )

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM earthquakes"
    )

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


# ---------------------------------------------------
# BUTTON 1 - FETCH EARTHQUAKE DATA
# ---------------------------------------------------

if st.button("🌐 Fetch Earthquake Data"):

    try:

        with st.spinner("Fetching data from USGS..."):

            data = get_earthquake_data(
                startdate,
                enddate
            )

            records = create_records(data)

            st.session_state["records"] = records

        st.success(
            f"✅ {len(records)} earthquake records fetched!"
        )

    except Exception as e:

        st.error(f"❌ Error: {e}")


# ---------------------------------------------------
# SHOW FIRST RECORD
# ---------------------------------------------------

if "records" in st.session_state:

    records = st.session_state["records"]

    st.subheader("First Earthquake Record")

    st.json(records[0])


# ---------------------------------------------------
# BUTTON 2 - CREATE DATABASE
# ---------------------------------------------------

if st.button("🗄️ Create Database"):

    try:

        create_database()

        st.success(
            "✅ earthquake_db database created successfully!"
        )

    except Exception as e:

        st.error(f"❌ Error: {e}")


# ---------------------------------------------------
# BUTTON 3 - CREATE TABLE
# ---------------------------------------------------

if st.button("📋 Create Earthquake Table"):

    try:

        create_database()

        create_table()

        st.success(
            "✅ earthquakes table created successfully!"
        )

    except Exception as e:

        st.error(f"❌ Error: {e}")


# ---------------------------------------------------
# BUTTON 4 - INSERT DATA
# ---------------------------------------------------

if st.button("📥 Insert Earthquake Data"):

    if "records" not in st.session_state:

        st.warning(
            "⚠️ First click 'Fetch Earthquake Data'."
        )

    else:

        try:

            records = st.session_state["records"]

            create_database()

            create_table()

            count = insert_data(records)

            st.success(
                f"✅ {count} records inserted successfully!"
            )

        except Exception as e:

            st.error(f"❌ Error: {e}")


# ---------------------------------------------------
# BUTTON 5 - DISPLAY MYSQL DATA
# ---------------------------------------------------

if st.button("📊 Show Database Data"):

    try:

        result = get_database_data()

        columns = [
            "id",
            "time",
            "updated",
            "latitude",
            "longitude",
            "depth_km",
            "mag",
            "magType",
            "place",
            "status",
            "tsunami",
            "alert",
            "felt",
            "cdi",
            "mmi",
            "sig",
            "net",
            "code",
            "ids",
            "sources",
            "types",
            "nst",
            "dmin",
            "rms",
            "gap",
            "type",
            "continent",
            "economic_loss"
        ]

        df = pd.DataFrame(
            result,
            columns=columns
        )

        st.subheader("Earthquake Database")

        st.write(
            f"Total records: {len(df)}"
        )

        st.dataframe(
            df,
            use_container_width=True
        )

    except Exception as e:

        st.error(f"❌ Error: {e}")