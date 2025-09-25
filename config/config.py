# --- 物理定数定義 ---
G0 = 9.80665 # 重力加速度 (m/s²)
RD = 287.058 # 乾燥空気の気体定数 (J/(kg·K))
EPSILON = 0.62198 # 水蒸気と乾燥空気の気体定数の比
ABS_ZERO_C = -273.15 # 絶対零度 (℃)

# --- ユーザー設定 ---
POINT_ID = "45212"
SENSOR_READ_INTERVAL = 15.0 # センサー読み取り間隔 (秒)
CALIBRATION_INTERVAL = 1800.0 # 校正間隔 (秒)
DEFAULT_SEA_LEVEL_PRESSURE = 1024.0 # デフォルトの海面気圧 (hPa)

# --- InfluxDB 設定 ---
INFLUXDB_URL = "" # e.g., "http://localhost:8086"
INFLUXDB_TOKEN = "" # e.g., "my-token"
INFLUXDB_ORG = "" # e.g., "my-org"
INFLUXDB_BUCKET = "" # e.g., "my-bucket"
