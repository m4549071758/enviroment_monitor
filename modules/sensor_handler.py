from datetime import datetime
from modules.altitude_handler import calculate_altitude_hypsometric
from modules.influx_handler import write_to_influxdb
from modules.disconfort_handler import disconfort_calculate
import adafruit_bme280
from modules.mhz19e_handler import MHZ19E

def read_sensor_data(bme280_sensor, co2_sensor, api):
    """センサーからデータを読み取り、表示し、InfluxDBに送信する。"""
    try:
        # CO2濃度の読み取り
        co2_ppm = 500.00  # デフォルト値
        if co2_sensor:
            co2_reading = co2_sensor.read_co2()
            if co2_reading is not None:
                co2_ppm = co2_reading
            else:
                print("警告: CO2センサーから読み取りできませんでした。デフォルト値を使用します")
        
        # BME280からすべてのデータを読み取り
        if bme280_sensor:
            try:
                temperature = bme280_sensor.temperature
                humidity = bme280_sensor.relative_humidity
                pressure = bme280_sensor.pressure
                altitude = bme280_sensor.altitude
            except Exception as e:
                print(f"エラー: BME280からデータを読み取りできませんでした: {e}")
                raise Exception("BME280センサーが利用できません")
        else:
            raise Exception("BME280センサーが利用できません")

        # 不快指数の計算
        disc_value = disconfort_calculate(temperature, humidity)

        # 気圧高度補正の計算
        corrected_altitude = calculate_altitude_hypsometric(bme280_sensor.sea_level_pressure, pressure, temperature, humidity)
        
        print(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            f"温度: {temperature:.2f} ℃, "
            f"湿度: {humidity:.2f} ％, "
            f"CO2濃度: {co2_ppm:.2f} ppm, "
            f"気圧: {pressure:.2f} hPa, "
            f"センサー高度: {altitude:.2f} m, "
            f"補正高度: {corrected_altitude:.2f} m, "
            f"(海面気圧補正値: {bme280_sensor.sea_level_pressure:.2f} hPa, センサー: BME280)"
        )

        write_to_influxdb(api, temperature, pressure, humidity, disc_value, co2_ppm)

    except (OSError, RuntimeError) as e:
        print(f"センサーからの読み取りエラー: {e}")
