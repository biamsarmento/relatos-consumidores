import mysql.connector
import pandas as pd
import glob
from datetime import datetime

TABELA = "relatos" # Nome da Tabela
FILE_PATH = './2024/*.csv' # Caminho para a pasta com os CSVs

def create_table_if_not_exists(connection):
    cursor = connection.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABELA} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            empresa VARCHAR(255),
            data DATE,
            local VARCHAR(255),
            status VARCHAR(255),
            relato TEXT,
            resposta TEXT,
            nota TEXT,
            comentario TEXT,
            UNIQUE KEY unique_record (empresa, data, local, status)
        )
    """)
    connection.commit()

def record_exists(connection, empresa, data, local, status):
    cursor = connection.cursor()
    cursor.execute(f"""
        SELECT 1 FROM {TABELA} 
        WHERE empresa = %s AND data = %s AND local = %s AND status = %s
    """, (empresa, data, local, status))
    return cursor.fetchone() is not None

def import_csv_to_db(file_path, connection):
    try:
        cursor = connection.cursor()
        data = pd.read_csv(file_path)
        
        # Substituir valores 'nan' por None
        data = data.where(pd.notnull(data), None)

        for _, row in data.iterrows():
            data_str = datetime.strptime(row['Data'], "%d/%m/%Y").strftime('%Y-%m-%d')
            if not record_exists(connection, row['Empresa'], data_str, row['Local'], row['Status']):
                cursor.execute(f"""
                    INSERT INTO {TABELA} (empresa, data, local, status, relato, resposta, nota, comentario)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    row['Empresa'], 
                    data_str, 
                    row['Local'], 
                    row['Status'], 
                    row['Relato'], 
                    row['Resposta'], 
                    row['Nota'], 
                    row['Comentario']
                ))
        connection.commit()
    except Exception as e:
        print(f"Error importing {file_path}: {e}")

def main():
    try:
        connection = mysql.connector.connect(
            host='localhost', # Insira o nome do host
            database='', # Insira o nome da base
            user='', # Insira o nome do usuário
            password='' # Insira a senha
        )

        if connection.is_connected():
            create_table_if_not_exists(connection)

            # Importar todos os arquivos CSV
            csv_files = glob.glob(FILE_PATH)
            for file in csv_files:
                import_csv_to_db(file, connection)
                
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            connection.close()

if __name__ == "__main__":
    main()
