import mh_z19

class MHZ19E:
    """MH-Z19E CO2センサーのハンドラークラス（mh-z19ライブラリ使用）"""
    
    def __init__(self):
        """
        MH-Z19Eセンサーを初期化
        """
        try:
            # ライブラリの初期化テスト（パラメータなしで呼び出し）
            test_reading = mh_z19.read_all()
            if test_reading is not None:
                print(f"MH-Z19Eセンサーを初期化しました。")
                self.available = True
            else:
                print(f"MH-Z19Eセンサーの初期化に失敗しました")
                self.available = False
        except Exception as e:
            print(f"MH-Z19Eセンサーの初期化に失敗しました: {e}")
            self.available = False
    
    def read_co2(self):
        """
        CO2濃度を読み取る
        
        Returns:
            float: CO2濃度 (ppm)、エラー時は None
        """
        if not self.available:
            return None
        
        try:
            # CO2濃度のみを読み取り
            reading = mh_z19.read()
            if reading is not None and 'co2' in reading:
                return float(reading['co2'])
            else:
                print("MH-Z19E: CO2データの読み取りに失敗しました")
                return None
                
        except Exception as e:
            print(f"MH-Z19E CO2読み取りエラー: {e}")
            return None
    
    def read_all(self):
        """
        全データを読み取る
        
        Returns:
            dict: {'co2': ppm値, 'temperature': 温度, 'TT': ?, 'SS': ?, 'UhUl': ?}、エラー時は None
        """
        if not self.available:
            return None
        
        try:
            reading = mh_z19.read_all()
            return reading
        except Exception as e:
            print(f"MH-Z19E 全データ読み取りエラー: {e}")
            return None
    
    
    def set_auto_calibration(self, enable=True):
        """
        自動校正の有効/無効を設定
        
        Args:
            enable (bool): True=自動校正有効、False=無効
        """
        if not self.available:
            print("センサーが利用できません")
            return False
        
        try:
            if enable:
                mh_z19.abc_on()
            else:
                mh_z19.abc_off()

            status = "有効" if enable else "無効"
            print(f"MH-Z19E: 自動校正を{status}にしました")
            return True
        except Exception as e:
            print(f"MH-Z19E 自動校正設定エラー: {e}")
            return False
    
    def get_range(self):
        """
        測定レンジを取得
        
        Returns:
            int: 測定レンジ（ppm）、エラー時は None
        """
        if not self.available:
            return None
        
        try:
            range_val = mh_z19.detection_range()
            return range_val
        except Exception as e:
            print(f"MH-Z19E レンジ取得エラー: {e}")
            return None
    
    def set_range(self, ppm_range):
        """
        測定レンジを設定
        
        Args:
            ppm_range (int): 測定レンジ（1000, 2000, 3000, 5000のいずれか）
        """
        if not self.available:
            print("センサーが利用できません")
            return False
        
        try:
            mh_z19.set_detection_range(ppm_range)
            print(f"MH-Z19E: 測定レンジを{ppm_range}ppmに設定しました")
            return True
        except Exception as e:
            print(f"MH-Z19E レンジ設定エラー: {e}")
            return False
    
    def close(self):
        """接続を閉じる（mh-z19ライブラリでは特に必要ない）"""
        if self.available:
            print("MH-Z19E接続を閉じました")
