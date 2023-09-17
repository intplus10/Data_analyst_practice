# !wget https://download.dremio.com/arrow-flight-sql-odbc-driver/arrow-flight-sql-odbc-driver-LATEST.x86_64.rpm
# !sudo yum localinstall -y arrow-flight-sql-odbc-driver-LATEST.x86_64.rpm 

import pyodbc
import pandas
import plotly.express as px
host = 'ft.vitesco.io'
port = 32010
uid = 'uic89063'
pwd = 'yourpwd'

# If you're using a MacOS, the driver is located here -> /Library/Dremio/ODBC/lib/libarrow-flight-sql-odbc.dylib; the below is for linux:
driver = "/opt/arrow-flight-sql-odbc-driver/lib64/libarrow-odbc.so.0.9.1.168"

# Set UseEncryption accordingly below:
DSN = "Dremio 64"
cnxn = pyodbc.connect(DSN=DSN, autocommit=True, PWD=pwd)
# cnxn = pyodbc.connect("Driver={};ConnectionType=Direct;HOST={};PORT={};AuthenticationType=Plain;UID={};PWD={}".format(driver, host, port,uid, pwd),autocommit=True, UseEncryption=False)

sql = 'SELECT * FROM FlatTable.DEB."Default"."DEB_STATION_DBASS138_L01S01_VAL_RECENT"'

mainFrame = pandas.read_sql(sql, cnxn)

print(mainFrame)
headerFrame = mainFrame.iloc[:0]
print(headerFrame)
colorSet = ["green", "red"]
selected_header = "M300-9"
chart1 = px.scatter(mainFrame,
                    x="timestamp", y=selected_header,
                    color="testrun_result", color_discrete_sequence=colorSet,
                    marginal_y="histogram")
chart1.add_hline(y=mainFrame[selected_header].median())
chart1.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1d",
                     step="day",
                     stepmode="backward"),
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)
chart1.show()
