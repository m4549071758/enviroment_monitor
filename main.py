# SPDX-FileCopyrightText: 2024
# SPDX-License-Identifier: MIT
from config.config import CALIBRATION_INTERVAL, POINT_ID, SENSOR_READ_INTERVAL
from modules.pressure_handler import get_latest_normal_pressure
from modules.sensor_handler import read_sensor_data
from init import bme280, co2_sensor, write_api, influx_client
import time

# --- メインループ ---
last_calibration_time = -CALIBRATION_INTERVAL
last_sensor_read_time = 0.0

print("\n--- メインループ開始 (停止するには Ctrl+C を押してください) ---")

try:
    while True:
        now = time.monotonic()
        
        # 校正チェック
        if now - last_calibration_time >= CALIBRATION_INTERVAL:
            last_calibration_time = now
            pressure_from_jma = get_latest_normal_pressure(POINT_ID)
            if pressure_from_jma is not None:
                bme280.sea_level_pressure = pressure_from_jma
                print(f"BME280センサー再校正完了。新しい海面気圧: {pressure_from_jma:.2f} hPa")
            else:
                print(f"警告: 校正に失敗。前回値{bme280.sea_level_pressure:.2f} hPaを使用します。")
            print("-" * 60)

        # センサー読み取りチェック
        if now - last_sensor_read_time >= SENSOR_READ_INTERVAL:
            last_sensor_read_time = now
            read_sensor_data(bme280, co2_sensor, write_api)
            
        # 動的なsleep時間計算（次のイベントまでの時間を計算）
        time_to_next_calibration = CALIBRATION_INTERVAL - (now - last_calibration_time)
        time_to_next_sensor_read = SENSOR_READ_INTERVAL - (now - last_sensor_read_time)
        
        # 次のイベントまでの最小時間を計算（最低0.1秒、最大1秒）
        next_event_time = min(time_to_next_calibration, time_to_next_sensor_read)
        sleep_time = max(0.1, min(1.0, next_event_time * 0.9))  # 少し早めに起きる
        
        time.sleep(sleep_time)

except KeyboardInterrupt:
    print("\nプログラムはユーザーにより停止されました。")
finally:
    # センサーの後処理
    if co2_sensor:
        co2_sensor.close()
    
    if 'influx_client' in locals() and influx_client:
        influx_client.close()
        print("InfluxDBクライアントをクローズしました。")