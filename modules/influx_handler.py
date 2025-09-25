from config.config import INFLUXDB_BUCKET, INFLUXDB_ORG
from influxdb_client import Point
from influxdb_client.client.exceptions import InfluxDBError

def write_to_influxdb(api, temp, press, hum, disconfort, co2):
    """InfluxDBにデータを書き込む。"""
    try:
        point = (
            Point("environment")
            .field("temperature", float(temp))
            .field("pressure", float(press))
            .field("humidity", float(hum))
            .field("disconfort", float(disconfort))
            .field("co2", float(co2))
        )
        api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
        return True
    except InfluxDBError as e:
        print(f"-> InfluxDBへの書き込みエラー: {e}")
        return False
    except Exception as e:
        print(f"-> InfluxDB書き込み中に予期せぬエラー: {e}")
        return False
