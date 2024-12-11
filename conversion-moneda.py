import yfinance as yf
import schedule
import time
import logging

# Configurar el registro
logging.basicConfig(
    filename="precio_dolar.log", 
    level=logging.INFO, 
    format="%(asctime)s - %(message)s"
)

def obtener_precio_dolar_yahoo():
    try:
        # Descargar los datos del tipo de cambio USD/ARS
        datos = yf.Ticker("USDARS=X")
        historial = datos.history(period="1d")  # Último día

        # Verificar si se recibieron datos
        if historial.empty:
            logging.warning("No se recibieron datos del historial.")
            return None

        # Extraer el precio de cierre más reciente
        precio_dolar = historial['Close'].iloc[-1]
        return round(precio_dolar, 2)
    except Exception as e:
        logging.error(f"Error al obtener los datos: {e}")
        return None

def actualizar_precio_dolar_yahoo():
    precio_dolar = obtener_precio_dolar_yahoo()
    if precio_dolar:
        mensaje = f"[Actualización] El precio del dólar es: {precio_dolar}"
        print(mensaje)
        logging.info(mensaje)
    else:
        logging.warning("No se pudo actualizar el precio del dólar.")

# Programar la tarea
schedule.every().hour.do(actualizar_precio_dolar_yahoo)

# Primera actualización manual
precio_dolar = obtener_precio_dolar_yahoo()
if precio_dolar:
    print(f"El precio inicial del dólar frente al peso argentino es: {precio_dolar}")

# Bucle de ejecución
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("\nPrograma terminado por el usuario.")
    logging.info("Programa terminado manualmente.")
