import click
import os
from dotenv import load_dotenv
import psycopg2
import csv


def conectar_a_postgresql():
  load_dotenv()
  try:
    connection = psycopg2.connect (
      host = os.getenv("DB_HOST"),
      port = os.getenv("DB_PORT"),
      dbname = os.getenv("DB_NAME"),
      user = os.getenv("DB_USER"),
      password = os.getenv("DB_PASSWORD")
    )
    cursor = connection.cursor()
    return connection, cursor
  except psycopg2.Error as error:
    print("\nError al conectarse a la base de datos:", error)
    return None, None

def ejecutar_consulta(connection, cursor, consulta):
  try:
    cursor.execute(consulta)
    connection.commit()
    print("\nConsulta ejecutada con éxito.")
  except psycopg2.Error as error:
    connection.rollback()
    print("\nError al ejecutar la consulta:", error)

def cerrar_conexion(connection, cursor):
  if cursor:
    cursor.close()
  if connection:
    connection.close()

def imprimir_grafico_barras(data_dict):
  max_valor = max(data_dict.values())
  for categoria, valor in data_dict.items():
    valor_porcentaje = (valor / max_valor) * 100
    barra = '#' * int(valor_porcentaje)
    print(f"{categoria:}: {barra} \n ({round(valor, 2)})")



@click.group()
def cli():
  pass

@cli.command()
def test():
  connection, cursor =  conectar_a_postgresql();
  if connection and cursor:
    consulta = "SELECT module_name FROM logs;"
    ejecutar_consulta(connection, cursor, consulta)
    resultados = cursor.fetchall()
    print("\n------------------------------\n");
    for fila in resultados:
      print(fila[0])
    print("\n------------------------------\n");
    cerrar_conexion(connection, cursor)

@cli.command(name="Update")
def Update():
  connection, cursor =  conectar_a_postgresql();
  if connection and cursor:
    consulta = """
      COPY logs(log_timestamp, log_level, module_name, api,func_name, log_message, elapsed_time_ms)
      FROM '/mnt/50A68CE3A68CCB44/UTEC/2023_2/Software_02/Semana08/Lab/soft_lab08/SEARCH_API/app.csv' DELIMITER ';';
    """
    route = '/mnt/50A68CE3A68CCB44/UTEC/2023_2/Software_02/Semana08/Lab/soft_lab08/SEARCH_API/app.csv'
    ejecutar_consulta(connection, cursor, consulta)
    with open(route, 'w') as archivo:
      archivo.write('')


@cli.command(name="CheckAvailability")
@click.option('--module_name', required=True, help="module's name")
@click.option('--last_days', required=False, help="days to analize")
@click.option('--interval_days', required=False, help="Interval days to analize")
@click.pass_context
def CheckAvailability(ctx, module_name, last_days, interval_days):
  if not module_name:
    ctx.fail('Se necesita el nombre de un módulo')
  else:
    if last_days:
      connection, cursor =  conectar_a_postgresql();
      consulta = f"""
        SELECT DATE(log_timestamp) AS fecha,
        log_level,
        COUNT(*) AS cantidad
        FROM logs
        WHERE module_name = '{module_name}'
          AND log_timestamp >= current_date - interval '{last_days} days' 
        GROUP BY fecha, log_level
        ORDER BY fecha DESC;
      """
      ejecutar_consulta(connection, cursor, consulta)
      resultados = cursor.fetchall()
      
      # Crear un diccionario para almacenar los resultados
      resultados_dict = {}
      
      # Iterar a través de los resultados y agregarlos al diccionario
      for fila in resultados:
        fecha, log_level, cantidad = fila
        if fecha not in resultados_dict:
          resultados_dict[fecha] = {}
        resultados_dict[fecha][log_level] = cantidad
      
      # Imprimir el diccionario de resultados
      # System availability = uptime / (uptime + downtime) * 100
      print("\n------------------------------\n")
      for fecha, valores in resultados_dict.items():
        print(f"{fecha}", end=": ")
        if(len(valores.items()) == 1):
          if 'WARNING' in valores:
            print("0%")
          else:
            print("100%")
        else:
          availability = (valores['INFO'] / (valores['INFO'] + valores['WARNING'])) * 100
          print(round(availability,2), end="%\n")
      print("\n------------------------------\n")
    elif interval_days:
      date_str_parts = interval_days.split('_TO_')
      start_date = date_str_parts[0]
      end_date = date_str_parts[1]

      connection, cursor =  conectar_a_postgresql();
      consulta = f"""
        SELECT DATE(log_timestamp) AS fecha,
        log_level,
        COUNT(*) AS cantidad
        FROM logs
        WHERE module_name = '{module_name}'
          AND log_timestamp >= '{start_date}'::date
          AND log_timestamp <= '{end_date}'::date + 1
        GROUP BY fecha, log_level
        ORDER BY fecha DESC;
      """
      ejecutar_consulta(connection, cursor, consulta)
      resultados = cursor.fetchall()
      
      # Crear un diccionario para almacenar los resultados
      resultados_dict = {}
      
      # Iterar a través de los resultados y agregarlos al diccionario
      for fila in resultados:
        fecha, log_level, cantidad = fila
        if fecha not in resultados_dict:
          resultados_dict[fecha] = {}
        resultados_dict[fecha][log_level] = cantidad
      
      # Imprimir el diccionario de resultados
      # System availability = uptime / (uptime + downtime) * 100
      print("\n------------------------------\n")
      for fecha, valores in resultados_dict.items():
        print(f"{fecha}", end=": ")
        if(len(valores.items()) == 1):
          if 'WARNING' in valores:
            print("0%")
          else:
            print("100%")
        else:
          availability = (valores['INFO'] / (valores['INFO'] + valores['WARNING'])) * 100
          print(round(availability,2), end="%\n")
      print("\n------------------------------\n")


@cli.command(name="CheckLatency")
@click.option('--module_name', required=True, help="module's name")
@click.option('--last_days', required=False, help="Past days to analize")
@click.option('--interval_days', required=False, help="Interval days to analize")
@click.pass_context
def CheckLatency(ctx, module_name, last_days, interval_days):
  if not module_name:
    ctx.fail('Se necesita el nombre de un módulo')
  else:
    if last_days:
      connection, cursor =  conectar_a_postgresql();
      consulta = f"""
        SELECT DATE(log_timestamp) AS fecha,
          AVG(elapsed_time_ms) AS promedio_elapsed_time
        FROM logs
        WHERE module_name = '{module_name}'
          AND log_timestamp >= current_date - interval '{last_days} days' 
        GROUP BY fecha
        ORDER BY fecha;
      """
      ejecutar_consulta(connection, cursor, consulta)
      resultados = cursor.fetchall()
      
      # Imprimir el diccionario de resultados
      # System availability = uptime / (uptime + downtime) * 100
      print("\n------------------------------\n")
      # Iterar a través de los resultados y agregarlos al diccionario
      for fila in resultados:
        fecha, promedio = fila
        print(fecha, end=": ")
        print(round(promedio, 2), end = " ms\n")
      print("\n------------------------------\n")
    elif interval_days:
      date_str_parts = interval_days.split('_TO_')
      start_date = date_str_parts[0]
      end_date = date_str_parts[1]
      
      connection, cursor =  conectar_a_postgresql();
      consulta = f"""
        SELECT DATE(log_timestamp) AS fecha,
        AVG(elapsed_time_ms) AS promedio_elapsed_time
        FROM logs
        WHERE module_name = '{module_name}'
              AND log_timestamp >= '{start_date}'::date
              AND log_timestamp <= '{end_date}'::date + 1
        GROUP BY fecha
        ORDER BY fecha;
      """
      ejecutar_consulta(connection, cursor, consulta)
      resultados = cursor.fetchall()
      
      # Imprimir el diccionario de resultados
      # System availability = uptime / (uptime + downtime) * 100
      print("\n------------------------------\n")
      # Iterar a través de los resultados y agregarlos al diccionario
      for fila in resultados:
        fecha, promedio = fila
        print(fecha, end=": ")
        print(round(promedio, 2), end = " ms\n")
      print("\n------------------------------\n")
    else:
      ctx.fail('Se necesita las opciones de --last_days o --interval_days')


@cli.command(name="RequestPerHour")
@click.option('--module_name', required=True, help="Module's name")
@click.option('--day', required=True, help="Day to analyse")
@click.pass_context
def RequestPerHour(ctx, module_name, day):
  if not module_name:
    ctx.fail('Se necesita el nombre de un módulo')
  else:
    connection, cursor =  conectar_a_postgresql();
    consulta = f"""
      SELECT
        EXTRACT(HOUR FROM log_timestamp) AS hour,
        COUNT(*) AS requests_per_hour
      FROM logs
      WHERE DATE(log_timestamp) = '{day}'
        AND module_name = '{module_name}'
      GROUP BY hour
      ORDER BY hour;
    """
    ejecutar_consulta(connection, cursor, consulta)
    resultados = cursor.fetchall()
    print("\n------------------------------\n");
    for fila in resultados:
      print(f"{fila[0]}: {fila[1]} request")
    print("\n------------------------------\n");
    cerrar_conexion(connection, cursor)

@cli.command(name="RenderGraph")
@click.option('--module_name', required=True, help="module's name")
@click.option('--mode', required=True, help="Availability, Latency or RequestPerHour")
@click.option('--last_days', required=False, help="Days to analize")
@click.option('--interval_days', required=False, help="Interval days to analize")
@click.option('--day', required=False, help="Day to analize")
@click.pass_context
def RenderGraph(ctx, module_name, mode, last_days, interval_days, day):
  if not module_name:
    ctx.fail('Se necesita el nombre de un módulo')
  if (mode == 'Availability'):
    connection, cursor =  conectar_a_postgresql();
    if last_days:
      consulta = f"""
        SELECT DATE(log_timestamp) AS fecha,
        log_level,
        COUNT(*) AS cantidad
        FROM logs
        WHERE module_name = '{module_name}'
          AND log_timestamp >= current_date - interval '{last_days} days' 
        GROUP BY fecha, log_level
        ORDER BY fecha DESC;
      """
      
    elif interval_days:
      date_str_parts = interval_days.split('_TO_')
      start_date = date_str_parts[0]
      end_date = date_str_parts[1]

      connection, cursor =  conectar_a_postgresql();
      consulta = f"""
        SELECT DATE(log_timestamp) AS fecha,
        log_level,
        COUNT(*) AS cantidad
        FROM logs
        WHERE module_name = '{module_name}'
          AND log_timestamp >= '{start_date}'::date
          AND log_timestamp <= '{end_date}'::date + 1
        GROUP BY fecha, log_level
        ORDER BY fecha DESC;
      """
    else:
      ctx.fail('Se necesita las opciones de --last_days o --interval_days')
    

    ejecutar_consulta(connection, cursor, consulta)
    resultados = cursor.fetchall()
    
    # Crear un diccionario para almacenar los resultados
    resultados_dict = {}
    
    # Iterar a través de los resultados y agregarlos al diccionario
    for fila in resultados:
      fecha, log_level, cantidad = fila
      if fecha not in resultados_dict:
        resultados_dict[fecha] = {}
      resultados_dict[fecha][log_level] = cantidad

    #Construir nuevo diccionario para imprimir
    reder_dict = {}

    for fecha, valores in resultados_dict.items():
      if(len(valores.items()) == 1):
        if 'WARNING' in valores:
          reder_dict[fecha] = 0
        else:
          reder_dict[fecha] = 100
      else:
        availability = (valores['INFO'] / (valores['INFO'] + valores['WARNING'])) * 100
        reder_dict[fecha] = availability

    # Imprimir el diccionario de resultados
    print("\n------------------------------\n")
    imprimir_grafico_barras(reder_dict)
    print("\n------------------------------\n")
  elif(mode == "Latency"):
    connection, cursor =  conectar_a_postgresql();
    if last_days: 
      consulta = f"""
        SELECT DATE(log_timestamp) AS fecha,
          AVG(elapsed_time_ms) AS promedio_elapsed_time
        FROM logs
        WHERE module_name = '{module_name}'
          AND log_timestamp >= current_date - interval '{last_days} days' 
        GROUP BY fecha
        ORDER BY fecha;
      """

    elif interval_days:
      date_str_parts = interval_days.split('_TO_')
      start_date = date_str_parts[0]
      end_date = date_str_parts[1]
      
      connection, cursor =  conectar_a_postgresql();
      consulta = f"""
        SELECT DATE(log_timestamp) AS fecha,
        AVG(elapsed_time_ms) AS promedio_elapsed_time
        FROM logs
        WHERE module_name = '{module_name}'
              AND log_timestamp >= '{start_date}'::date
              AND log_timestamp <= '{end_date}'::date + 1
        GROUP BY fecha
        ORDER BY fecha;
      """
    else:
      ctx.fail('Se necesita las opciones de --last_days o --interval_days')

    ejecutar_consulta(connection, cursor, consulta)
    resultados = cursor.fetchall()

    # Crear un diccionario para almacenar los resultados
    resultados_dict = {}
    
    # Iterar a través de los resultados y agregarlos al diccionario
    for fila in resultados:
      fecha, promedio = fila
      if fecha not in resultados_dict:
        resultados_dict[fecha] = {}
      resultados_dict[fecha] = promedio

    # Imprimir el diccionario de resultados
    print("\n------------------------------\n")
    imprimir_grafico_barras(resultados_dict)
    print("\n------------------------------\n")
  elif (mode == "RequestPerHour"):
    connection, cursor =  conectar_a_postgresql();
    consulta = f"""
      SELECT
        EXTRACT(HOUR FROM log_timestamp) AS hour,
        COUNT(*) AS requests_per_hour
      FROM logs
      WHERE DATE(log_timestamp) = '{day}'
        AND module_name = '{module_name}'
      GROUP BY hour
      ORDER BY hour;
    """
    ejecutar_consulta(connection, cursor, consulta)
    resultados = cursor.fetchall()
    
    # Crear un diccionario para almacenar los resultados
    resultados_dict = {}
    
    # Iterar a través de los resultados y agregarlos al diccionario
    for fila in resultados:
      hora, request = fila
      if hora not in resultados_dict:
        resultados_dict[hora] = {}
      resultados_dict[hora] = request

    # Imprimir el diccionario de resultados
    print("\n------------------------------\n")
    imprimir_grafico_barras(resultados_dict)
    print("\n------------------------------\n")

  else:
    ctx.fail('Parámetro "mode" incorrecto: Latency or Availability')


def escribir_csv_availability(datos, nombre_archivo):
  with open(nombre_archivo, 'w', newline='') as archivo_csv:
    # Crear un objeto escritor CSV
    escritor_csv = csv.writer(archivo_csv)

    # Escribir la cabecera del CSV (nombres de las columnas)
    escritor_csv.writerow(['Fecha', 'Availability'])

    # Escribir los datos del diccionario como filas en el CSV
    for fecha, valor in datos.items():
      escritor_csv.writerow([fecha, valor])

def escribir_csv_latency(datos, nombre_archivo):
  with open(nombre_archivo, 'w', newline='') as archivo_csv:
    # Crear un objeto escritor CSV
    escritor_csv = csv.writer(archivo_csv)

    # Escribir la cabecera del CSV (nombres de las columnas)
    escritor_csv.writerow(['Fecha', 'Latency'])

    # Escribir los datos del diccionario como filas en el CSV
    for fecha, valor in datos.items():
      escritor_csv.writerow([fecha, valor])

def escribir_csv_request_hour(datos, nombre_archivo):
  with open(nombre_archivo, 'w', newline='') as archivo_csv:
    # Crear un objeto escritor CSV
    escritor_csv = csv.writer(archivo_csv)

    # Escribir la cabecera del CSV (nombres de las columnas)
    escritor_csv.writerow(['Hora', 'Requests'])

    # Escribir los datos del diccionario como filas en el CSV
    for fecha, valor in datos.items():
      escritor_csv.writerow([fecha, valor])

# New Implementation
@cli.command(name="GenerateReport")
@click.option('--module_name', required=True, help="module's name")
@click.option('--mode', required=True, help="Availability, Latency or RequestPerHour")
@click.option('--last_days', required=False, help="Days to analize")
@click.option('--interval_days', required=False, help="Interval days to analize")
@click.option('--day', required=False, help="Day to analize")
@click.pass_context
def GenerateReport(ctx, module_name, mode, last_days, interval_days, day):
  if not module_name:
    ctx.fail('Se necesita el nombre de un módulo')
  if (mode == 'Availability'):
    connection, cursor =  conectar_a_postgresql();
    if last_days:
      consulta = f"""
        SELECT DATE(log_timestamp) AS fecha,
        log_level,
        COUNT(*) AS cantidad
        FROM logs
        WHERE module_name = '{module_name}'
          AND log_timestamp >= current_date - interval '{last_days} days' 
        GROUP BY fecha, log_level
        ORDER BY fecha DESC;
      """
      
    elif interval_days:
      date_str_parts = interval_days.split('_TO_')
      start_date = date_str_parts[0]
      end_date = date_str_parts[1]

      connection, cursor =  conectar_a_postgresql();
      consulta = f"""
        SELECT DATE(log_timestamp) AS fecha,
        log_level,
        COUNT(*) AS cantidad
        FROM logs
        WHERE module_name = '{module_name}'
          AND log_timestamp >= '{start_date}'::date
          AND log_timestamp <= '{end_date}'::date + 1
        GROUP BY fecha, log_level
        ORDER BY fecha DESC;
      """
    else:
      ctx.fail('Se necesita las opciones de --last_days o --interval_days')
    

    ejecutar_consulta(connection, cursor, consulta)
    resultados = cursor.fetchall()
    
    # Crear un diccionario para almacenar los resultados
    resultados_dict = {}
    
    # Iterar a través de los resultados y agregarlos al diccionario
    for fila in resultados:
      fecha, log_level, cantidad = fila
      if fecha not in resultados_dict:
        resultados_dict[fecha] = {}
      resultados_dict[fecha][log_level] = cantidad

    #Construir nuevo diccionario para imprimir
    reder_dict = {}

    for fecha, valores in resultados_dict.items():
      if(len(valores.items()) == 1):
        if 'WARNING' in valores:
          reder_dict[fecha] = 0
        else:
          reder_dict[fecha] = 100
      else:
        availability = (valores['INFO'] / (valores['INFO'] + valores['WARNING'])) * 100
        reder_dict[fecha] = availability

    # Generar CSV
    nombre_del_archivo = 'AvailabilityReport.csv'
    escribir_csv_availability(reder_dict, nombre_del_archivo)
    print("Reporte Generado con éxito :D")


  elif(mode == "Latency"):
    connection, cursor =  conectar_a_postgresql();
    if last_days: 
      consulta = f"""
        SELECT DATE(log_timestamp) AS fecha,
          AVG(elapsed_time_ms) AS promedio_elapsed_time
        FROM logs
        WHERE module_name = '{module_name}'
          AND log_timestamp >= current_date - interval '{last_days} days' 
        GROUP BY fecha
        ORDER BY fecha;
      """

    elif interval_days:
      date_str_parts = interval_days.split('_TO_')
      start_date = date_str_parts[0]
      end_date = date_str_parts[1]
      
      connection, cursor =  conectar_a_postgresql();
      consulta = f"""
        SELECT DATE(log_timestamp) AS fecha,
        AVG(elapsed_time_ms) AS promedio_elapsed_time
        FROM logs
        WHERE module_name = '{module_name}'
              AND log_timestamp >= '{start_date}'::date
              AND log_timestamp <= '{end_date}'::date + 1
        GROUP BY fecha
        ORDER BY fecha;
      """
    else:
      ctx.fail('Se necesita las opciones de --last_days o --interval_days')

    ejecutar_consulta(connection, cursor, consulta)
    resultados = cursor.fetchall()

    # Crear un diccionario para almacenar los resultados
    resultados_dict = {}
    
    # Iterar a través de los resultados y agregarlos al diccionario
    for fila in resultados:
      fecha, promedio = fila
      if fecha not in resultados_dict:
        resultados_dict[fecha] = {}
      resultados_dict[fecha] = promedio

    # Generar CSV
    nombre_del_archivo = 'LatencyReport.csv'
    escribir_csv_latency(resultados_dict, nombre_del_archivo)
    print("Reporte Generado con éxito :D")

  elif (mode == "RequestPerHour"):
    connection, cursor =  conectar_a_postgresql();
    consulta = f"""
      SELECT
        EXTRACT(HOUR FROM log_timestamp) AS hour,
        COUNT(*) AS requests_per_hour
      FROM logs
      WHERE DATE(log_timestamp) = '{day}'
        AND module_name = '{module_name}'
      GROUP BY hour
      ORDER BY hour;
    """
    ejecutar_consulta(connection, cursor, consulta)
    resultados = cursor.fetchall()
    
    # Crear un diccionario para almacenar los resultados
    resultados_dict = {}
    
    # Iterar a través de los resultados y agregarlos al diccionario
    for fila in resultados:
      hora, request = fila
      if hora not in resultados_dict:
        resultados_dict[hora] = {}
      resultados_dict[hora] = request

    # Generar CSV
    nombre_del_archivo = 'RequestPerHourReport.csv'
    escribir_csv_request_hour(resultados_dict, nombre_del_archivo)
    print("Reporte Generado con éxito :D")

  else:
    ctx.fail('Parámetro "mode" incorrecto: Latency or Availability')

if __name__ == '__main__':
  cli()