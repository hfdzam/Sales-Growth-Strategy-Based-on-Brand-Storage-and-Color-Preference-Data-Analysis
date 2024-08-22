from airflow.models import DAG
from airflow.operators.python import PythonOperator
#from airflow.providers.postgres.operators.postgres import PostgresOperator
# from airflow.utils.task_group import TaskGroup
from datetime import datetime
from sqlalchemy import create_engine #koneksi ke postgres
import pandas as pd

from elasticsearch import Elasticsearch

def csv_to_postgres():
 
    database = "airflow_m3"
    username = "airflow_m3"
    password = "airflow_m3"
    host = "postgres"

    # Membuat URL koneksi PostgreSQL
    postgres_url = f"postgresql+psycopg2://{username}:{password}@{host}/{database}"

    # Gunakan URL ini saat membuat koneksi SQLAlchemy
    engine = create_engine(postgres_url)
    # engine= create_engine("postgresql+psycopg2://airflow:airflow@postgres/airflow")
    conn = engine.connect()

    data = pd.read_csv('/opt/airflow/dags/P2M3_Hafidz_Masruri_data_raw.csv')
    #df.to_sql(nama_table_db, conn, index=False, if_exists='replace')
    data.to_sql('table_sales', conn, 
              index=False, 
              if_exists='replace')  # M
    
    '''----------------------------------------------------------------------------------------------'''
#ambil data 
def get():
    '''fungsi untuk mengambil data'''
    # Gunakan URL ini saat membuat koneksi SQLAlchemy
    database = "airflow_m3"
    username = "airflow_m3"
    password = "airflow_m3"
    host = "postgres"

    # Membuat URL koneksi PostgreSQL
    postgres_url = f"postgresql+psycopg2://{username}:{password}@{host}/{database}"

    engine = create_engine(postgres_url)
    conn = engine.connect()

    data = pd.read_sql_query("select * from table_sales", conn) #nama table sesuaikan sama nama table di postgres

    data.to_csv('/opt/airflow/dags/New_Hafidz.csv', sep=',', index=False)
    


def clean(): 
    ''' fungsi untuk membersihkan data'''
    # ambil data
    data = pd.read_csv("/opt/airflow/dags/New_Hafidz.csv")
     
    # dropna terlebih dahulu agar tidak ada nan
    data.dropna(inplace=True)
    print('drop sukses') 

    # bersihkan colom
    data.columns = (data.columns
                    .str.lower()  # nama kolom kecil
                    .str.replace(' ', '_', regex=False)  # spasi ganti '_'
                    .str.replace(r'[^a-zA-Z0-9_]', '', regex=True)) # hapus simbol
    print('colom update sukses')

    # hapus kolom models karena isinya sama dengan mobile
    data = data.drop(columns=['models'])
    print('Kolom models sukses dihapus')

    # drop duplikat karena sudah di convert kejumlah terjual
    data = data.drop_duplicates()
    print('drop duplicate sukses')

    # Add unique 'id'
    data['id'] = range(1, len(data) + 1)
    print('id kolom sukses')

    # hapus sepasi di belakang nama
    columns_to_strip = ['brands', 'colors', 'mobile']  # Tambahkan kolom lain jika diperlukan
    for column in columns_to_strip:
        if column in data.columns:
            data[column] = data[column].astype(str).str.rstrip()

    data.to_csv('/opt/airflow/dags/P2M3_hafidz_masruri_data_clean.csv', index=False)
    
def up_elasticsearch():
    es = Elasticsearch("http://elasticsearch:9200")
    data = pd.read_csv('/opt/airflow/dags/P2M3_hafidz_masruri_data_clean')
    
    for i, r in data.iterrows():
        doc = r.to_dict()  # Convert the row to a dictionary
        res = es.index(index="table_sales", id=i+1, body=doc)
        print(f"Response from Elasticsearch: {res}")
    

    '''---------------------------------------------------------------------------------------------------'''


default_args = {
    'owner': 'Hafidz', 
    'start_date': datetime(1999, 9, 23, 20, 00) #jangan hari sekarang
                            # ganti hari lahir saja hehe
}

with DAG(
    "P2M3_Hafidz_DAG_hck", #atur sesuai nama project kalian
    description='Milestone_3',
    schedule_interval='30 6 * * *', #6.30 atur schedule untuk menjalankan airflow pada 06:30.
    default_args=default_args, 
    catchup=False
) as dag:
    
    # Task : 1 memindahkan data untuk postgres
    '''Fungsi untuk menaruh data pada postgres'''
    csv_task = PythonOperator(
        task_id='csv_to_postgres',
        python_callable=csv_to_postgres) #sesuaikan dengan nama fungsi yang kalian buat
    '''-------------------------------------------------------------------------------------------------------'''
    #task: 2
    '''Fungsi ini untuk mengambil data pada postfres'''
    get_data = PythonOperator(
        task_id='ambil_data_postgres',
        python_callable=get) #
    

    # Task: 3
    ''' Fungsi ini untuk cleaning data'''
    clean_data = PythonOperator(
        task_id='clean_data',
        python_callable=clean)

    # Task: 4
    ''' Fungsi ini untuk update data ke elastic'''
    update = PythonOperator(
        task_id='update_to_elastic',
        python_callable=up_elasticsearch)

    #proses untuk menjalankan di airflow
    csv_task >> get_data >> clean_data >> update
