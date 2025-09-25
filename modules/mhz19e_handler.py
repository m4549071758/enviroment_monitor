import mh_z19

class MHZ19E:
    """MH-Z19E CO2センサーのハンドラークラス（mh-z19ライブラリ使用）"""
    
    def __init__(self, serial_device='/dev/serial0'):
        """
        MH-Z19Eセンサーを初期化
        
        Args:
            serial_device (str): シリアルデバイス（デフォルト: /dev/serial0）
        """
        self.serial_device = serial_device
        try:
            # ライブラリの初期化
            test_reading = mh_z19.read_all(serial_device=serial_device)
            if test_reading is not None:
                print(f"MH-Z19Eセンサーを初期化しました。デバイス: {serial_device}")
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
            reading = mh_z19.read(serial_device=self.serial_device)
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
            reading = mh_z19.read_all(serial_device=self.serial_device)
            return reading
        except Exception as e:
            print(f"MH-Z19E 全データ読み取りエラー: {e}")
            return None
    
    def calibrate_zero(self):
        """
        ゼロポイント校正を実行（400ppmの環境で使用）
        """
        if not self.available:
            print("センサーが利用できません")
            return False
        
        try:
            mh_z19.zero_point_calibration(serial_device=self.serial_device)
            print("MH-Z19E: ゼロポイント校正を実行しました")
            return True
        except Exception as e:
            print(f"MH-Z19E 校正エラー: {e}")
            return False
    
    def calibrate_span(self, ppm):
        """
        スパン校正を実行
        
        Args:
            ppm (int): 校正用ガス濃度
        """
        if not self.available:
            print("センサーが利用できません")
            return False
        
        try:
            mh_z19.span_point_calibration(ppm, serial_device=self.serial_device)
            print(f"MH-Z19E: スパン校正を実行しました (基準: {ppm}ppm)")
            return True
        except Exception as e:
            print(f"MH-Z19E スパン校正エラー: {e}")
            return False
    
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
                mh_z19.abc_on(serial_device=self.serial_device)
            else:
                mh_z19.abc_off(serial_device=self.serial_device)
            
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
            range_val = mh_z19.detection_range(serial_device=self.serial_device)
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
            mh_z19.set_detection_range(ppm_range, serial_device=self.serial_device)
            print(f"MH-Z19E: 測定レンジを{ppm_range}ppmに設定しました")
            return True
        except Exception as e:
            print(f"MH-Z19E レンジ設定エラー: {e}")
            return False
    
    def close(self):
        """接続を閉じる（mh-z19ライブラリでは特に必要ない）"""
        if self.available:
            print("MH-Z19E接続を閉じました")