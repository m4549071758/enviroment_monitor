from config.config import DEFAULT_SEA_LEVEL_PRESSURE, INFLUXDB_ORG, INFLUXDB_TOKEN, INFLUXDB_URL
from adafruit_bme280 import basic as adafruit_bme280
import board
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from modules.mhz19e_handler import MHZ19E


# --- センサー初期化 ---
try:
    i2c = board.I2C()
except Exception as e:
    print(f"I2Cの初期化に失敗しました: {e}")
    exit()

# BME280センサー初期化
try:
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)  # アドレスは0x76または0x77
    bme280.sea_level_pressure = DEFAULT_SEA_LEVEL_PRESSURE
    print(f"BME280センサーを初期化しました。規正海面気圧: {DEFAULT_SEA_LEVEL_PRESSURE} hPa")
except (ValueError, RuntimeError) as e:
    print(f"BME280センサーの初期化に失敗しました: {e}")
    try:
        # アドレス0x77で再試行
        bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x77)
        bme280.sea_level_pressure = DEFAULT_SEA_LEVEL_PRESSURE
        print(f"BME280センサーを初期化しました（アドレス0x77）。規正海面気圧: {DEFAULT_SEA_LEVEL_PRESSURE} hPa")
    except (ValueError, RuntimeError) as e2:
        print(f"BME280センサーの初期化に完全に失敗しました: {e2}")
        bme280 = None

# MH-Z19Eセンサー初期化
try:
    co2_sensor = MHZ19E()  # Raspberry Piのシリアルポート
    if co2_sensor.available:
        co2_sensor.set_auto_calibration(True)  # 自動校正を有効にする
        print("MH-Z19E CO2センサーを初期化しました")
    else:
        co2_sensor = None
except Exception as e:
    print(f"MH-Z19E CO2センサーの初期化に失敗しました: {e}")
    co2_sensor = None

# --- InfluxDBクライアント初期化 ---
try:
    influx_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
    write_api = influx_client.write_api(write_options=SYNCHRONOUS)
    print(f"InfluxDBに接続しました (URL: {INFLUXDB_URL}, Org: {INFLUXDB_ORG})")
except Exception as e:
    print(f"InfluxDBクライアントの初期化に失敗しました: {e}")
    exit()

# 利用可能なセンサーを確認
if not bme280:
    print("エラー: BME280センサーが利用できません")
    exit()

if not co2_sensor:
    print("警告: MH-Z19E CO2センサーが利用できません。CO2データは固定値を使用します")
