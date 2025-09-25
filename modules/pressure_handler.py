import requests
from datetime import datetime, timedelta, timezone

def get_latest_normal_pressure(point_id: str) -> float | None:
    """
    気象庁のAMeDAS JSONデータから最新の「海面更正気圧(normalPressure)」を取得する。
    """
    try:
        jst = timezone(timedelta(hours=9))
        now_jst = datetime.now(jst)
        json_hour = (now_jst.hour // 3) * 3
        date_str = now_jst.strftime('%Y%m%d')
        
        url = f"https://www.jma.go.jp/bosai/amedas/data/point/{point_id}/{date_str}_{json_hour:02d}.json"
        
        print(f"\n校正データ取得中: {url}")
            
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()

        if not data:
            print("警告: JSONデータが空です。")
            return None
            
        latest_timestamp_key = sorted(data.keys())[-1]
        latest_data = data[latest_timestamp_key]
        
        normal_pressure_list = latest_data.get("normalPressure")

        if normal_pressure_list and isinstance(normal_pressure_list, list) and len(normal_pressure_list) > 0:
            normal_pressure = normal_pressure_list[0]
            if normal_pressure is not None:
                dt_str = datetime.strptime(latest_timestamp_key, "%Y%m%d%H%M%S").strftime('%Y-%m-%d %H:%M:%S')
                print(f"正常気圧データ取得成功: {dt_str}")
                return float(normal_pressure)
        
        print("警告: 最新データに 'normalPressure' が見つかりません。")
        return None

    except requests.exceptions.RequestException as e:
        print(f"警告: ネットワークエラー: {e}")
        return None
    except (ValueError, KeyError, IndexError) as e:
        print(f"警告: JSON解析またはキー取得失敗: {e}")
        return None
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
        return None
    