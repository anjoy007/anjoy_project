import requests
import sqlite3
import pandas as pd

service_key = 'z03Phci3d+Tw058gpjJ9kqAmO4uwoVX8jnxXSnX0gdyFm2ATfbH1BAOujb6kSEsTuARcjexI7qOczP5Ur+QcsQ=='
base_url = 'https://api.data.go.kr/openapi/tn_pubr_public_solar_gen_flct_api'

conn = sqlite3.connect('solar_full.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS solar (
    facility_name TEXT, address_lot TEXT, x_coord REAL, y_coord REAL,
    status TEXT, capacity REAL, supply_voltage REAL, frequency INTEGER,
    installation_year INTEGER, permit_date TEXT
)''')

page = 1
per_page = 100
while True:
    params = {
        'page': page,
        'perPage': per_page,
        'serviceKey': service_key,
        'returnType': 'JSON'
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    items = data.get('data', [])
    if not items:
        break
    for item in items:
        cursor.execute('INSERT INTO solar VALUES (?,?,?,?,?,?,?,?,?,?)', (
            item.get('태양광발전시설명'),
            item.get('소재지지번주소'),
            item.get('X좌표'),
            item.get('Y좌표'),
            item.get('가동상태구분명'),
            item.get('설비용량'),
            item.get('공급전압'),
            item.get('주파수'),
            item.get('설치연도'),
            item.get('허가일자')
        ))
    conn.commit()
    page += 1

df = pd.read_sql_query('SELECT * FROM solar', conn)
df.to_excel('solar_full.xlsx', index=False)
conn.close()
