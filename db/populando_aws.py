import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os
from time import time
import traceback

def log_message(message):
    """Formata mensagens de log para melhor visualização"""
    print(f"[{time():.2f}] {message}")

def load_data_with_logs():
    # Carrega os dados CSV com verificação
    log_message("INICIANDO CARGA DE DADOS")
    log_message("Carregando arquivos CSV...")
    
    try:
        start_time = time()
        df_cliente = pd.read_csv(r"C:\Users\André Ciccozzi\OneDrive\Documentos\Banking\Analise-AML\data\data_limpos\clientes_agencia_londrina_limpo.csv")
        log_message(f"Clientes carregados - {len(df_cliente)} registros | Tempo: {time()-start_time:.2f}s")
        
        start_time = time()
        df_abril = pd.read_csv(r"C:\Users\André Ciccozzi\OneDrive\Documentos\Banking\Analise-AML\data\data_limpos\transacoes_abril_2025_limpo.csv")
        log_message(f"Transações de abril carregadas - {len(df_abril)} registros | Tempo: {time()-start_time:.2f}s")
        
        start_time = time()
        df_maio = pd.read_csv(r"C:\Users\André Ciccozzi\OneDrive\Documentos\Banking\Analise-AML\data\data_limpos\transacoes_maio_2025_limpo.csv")
        log_message(f"Transações de maio carregadas - {len(df_maio)} registros | Tempo: {time()-start_time:.2f}s")
        
        start_time = time()
        df_junho = pd.read_csv(r"C:\Users\André Ciccozzi\OneDrive\Documentos\Banking\Analise-AML\data\data_limpos\transacoes_junho_2025_limpo.csv")
        log_message(f"Transações de junho carregadas - {len(df_junho)} registros | Tempo: {time()-start_time:.2f}s")
    except Exception as e:
        log_message(f"ERRO AO CARREGAR ARQUIVOS CSV: {str(e)}")
        traceback.print_exc()
        return

    # Configuração do banco de dados
    log_message("\nCONFIGURANDO CONEXÃO COM O BANCO DE DADOS")
    load_dotenv()
    
    try:
        config = {
            'host': os.getenv("MYSQL_HOST"),
            'port': int(os.getenv("MYSQL_PORT")),
            'user': os.getenv("MYSQL_USER"),
            'password': os.getenv("MYSQL_PASSWORD"),
            'database': os.getenv("MYSQL_DATABASE"),
            'allow_local_infile': True
        }
        
        log_message("Tentando conectar ao MySQL...")
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        log_message("Conexão estabelecida com sucesso!")
    except Exception as e:
        log_message(f"ERRO NA CONEXÃO COM O BANCO: {str(e)}")
        traceback.print_exc()
        return

    # Otimizações para inserção rápida
    log_message("\nOTIMIZANDO CONFIGURAÇÕES PARA CARGA RÁPIDA")
    try:
        cursor.execute("SET autocommit = 0")
        cursor.execute("SET unique_checks = 0")
        cursor.execute("SET foreign_key_checks = 0")
        log_message("Configurações otimizadas para carga rápida")
    except Exception as e:
        log_message(f"AVISO: Não foi possível otimizar configurações: {str(e)}")

    # Método 1: LOAD DATA LOCAL INFILE (mais rápido)
    log_message("\nTENTANDO MÉTODO RÁPIDO (LOAD DATA LOCAL INFILE)")
    temp_files = []
    
    try:
        # Salva DataFrames como arquivos temporários
        log_message("Criando arquivos temporários...")
        for df, name in [(df_cliente, 'clientes'), (df_abril, 'abril'), (df_maio, 'maio'), (df_junho, 'junho')]:
            temp_file = f"temp_{name}.csv"
            try:
                df.to_csv(temp_file, index=False, header=False)
                temp_files.append(temp_file)
                log_message(f"Arquivo temporário criado: {temp_file} | Tamanho: {os.path.getsize(temp_file)/1024:.2f} KB")
            except Exception as e:
                log_message(f"ERRO ao criar {temp_file}: {str(e)}")
                raise

        # Insere clientes
        log_message("\nINSERINDO CLIENTES...")
        start_time = time()
        cursor.execute(f"""
            LOAD DATA LOCAL INFILE 'temp_clientes.csv'
            INTO TABLE cliente
            FIELDS TERMINATED BY ','
            LINES TERMINATED BY '\n'
            (id_cliente, nome, data_nascimento, cidade_residencia, tipo_conta, pessoa_fisica, score_credito)
        """)
        conn.commit()
        log_message(f"Clientes inseridos com sucesso! | Tempo: {time()-start_time:.2f}s | Linhas: {len(df_cliente)}")

        # Insere transações
        for file, df, month in zip(['temp_abril.csv', 'temp_maio.csv', 'temp_junho.csv'], 
                                 [df_abril, df_maio, df_junho], 
                                 ['abril', 'maio', 'junho']):
            log_message(f"\nINSERINDO TRANSAÇÕES DE {month.upper()}...")
            start_time = time()
            cursor.execute(f"""
                LOAD DATA LOCAL INFILE '{file}'
                INTO TABLE transacao
                FIELDS TERMINATED BY ','
                LINES TERMINATED BY '\n'
                (id_transacao, id_cliente_origem, id_cliente_destino, data_transacao, valor, canal, cidade_transacao, flag_suspeita, flag_fraude_confirmada)
            """)
            conn.commit()
            log_message(f"Transações de {month} inseridas com sucesso! | Tempo: {time()-start_time:.2f}s | Linhas: {len(df)}")

        log_message("\nCARGA DE DADOS CONCLUÍDA COM SUCESSO VIA LOAD DATA!")

    except mysql.connector.Error as e:
        log_message(f"\nFALHA NO MÉTODO RÁPIDO: {str(e)}")
        traceback.print_exc()
        conn.rollback()
        log_message("Tentando método alternativo (executemany)...")
        
        # Método 2: executemany (segunda melhor opção)
        try:
            # Insere clientes
            log_message("\nINSERINDO CLIENTES (MÉTODO EXECUTEMANY)...")
            start_time = time()
            clientes_data = [tuple(x) for x in df_cliente.to_numpy()]
            
            try:
                cursor.executemany(
                    "INSERT INTO cliente (id_cliente, nome, data_nascimento, cidade_residencia, tipo_conta, pessoa_fisica, score_credito) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    clientes_data
                )
                conn.commit()
                log_message(f"Clientes inseridos com sucesso! | Tempo: {time()-start_time:.2f}s | Linhas: {len(clientes_data)}")
            except Exception as e:
                log_message(f"ERRO ao inserir clientes: {str(e)}")
                traceback.print_exc()
                conn.rollback()
                raise

            # Insere transações em lotes
            for df, month in zip([df_abril, df_maio, df_junho], ['abril', 'maio', 'junho']):
                log_message(f"\nINSERINDO TRANSAÇÕES DE {month.upper()}...")
                start_time = time()
                transacoes_data = [tuple(x) for x in df.to_numpy()]
                
                batch_size = 10000
                total_rows = len(transacoes_data)
                inserted_rows = 0
                
                for i in range(0, total_rows, batch_size):
                    batch = transacoes_data[i:i+batch_size]
                    try:
                        cursor.executemany(
                            "INSERT INTO transacao (id_transacao, id_cliente_origem, id_cliente_destino, data_transacao, valor, canal, cidade_transacao, flag_suspeita, flag_fraude_confirmada) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            batch
                        )
                        conn.commit()
                        inserted_rows += len(batch)
                        log_message(f"Lote {i//batch_size + 1} de {month} inserido | Progresso: {inserted_rows}/{total_rows} ({inserted_rows/total_rows*100:.1f}%)")
                    except Exception as e:
                        log_message(f"ERRO no lote {i//batch_size + 1} de {month}: {str(e)}")
                        traceback.print_exc()
                        conn.rollback()
                        raise
                
                log_message(f"Transações de {month} concluídas! | Tempo total: {time()-start_time:.2f}s")

            log_message("\nCARGA DE DADOS CONCLUÍDA COM SUCESSO VIA EXECUTEMANY!")

        except Exception as e:
            log_message(f"\nERRO GRAVE: Falha no método executemany: {str(e)}")
            traceback.print_exc()
            conn.rollback()

    finally:
        # Restaura configurações
        try:
            cursor.execute("SET autocommit = 1")
            cursor.execute("SET unique_checks = 1")
            cursor.execute("SET foreign_key_checks = 1")
            log_message("Configurações do MySQL restauradas")
        except Exception as e:
            log_message(f"AVISO: Não foi possível restaurar configurações: {str(e)}")

        # Remove arquivos temporários
        log_message("\nLIMPANDO ARQUIVOS TEMPORÁRIOS...")
        for file in temp_files:
            try:
                os.remove(file)
                log_message(f"Arquivo removido: {file}")
            except Exception as e:
                log_message(f"AVISO: Não foi possível remover {file}: {str(e)}")

        # Fecha conexão
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            log_message("Conexão com o banco de dados encerrada")
        
        log_message("PROCESSO FINALIZADO")

if __name__ == "__main__":
    load_data_with_logs()