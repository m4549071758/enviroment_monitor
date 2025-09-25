from config.config import ABS_ZERO_C, EPSILON, G0, RD
import math

def calculate_virtual_temperature(temperature_c: float, relative_humidity_pct: float, pressure_hpa: float) -> float:
    if temperature_c <= ABS_ZERO_C:
        raise ValueError("Temperature must be above absolute zero.")
    if not (0 <= relative_humidity_pct <= 100):
        raise ValueError("Relative humidity must be between 0 and 100.")
    if pressure_hpa <= 0:
        raise ValueError("Pressure must be positive.")

    es = 6.1078 * (10 ** ((7.5 * temperature_c) / (237.3 + temperature_c)))

    e = es * (relative_humidity_pct / 100.0)

    if e >= pressure_hpa:
        e = pressure_hpa * 0.999 
    
    r = (EPSILON * e) / (pressure_hpa - e)

    temperature_k = temperature_c + 273.15
    tv_k = temperature_k * (1 + r / EPSILON) / (1 + r)
    
    return tv_k

def calculate_altitude_hypsometric(pressure_sea_level_hpa: float, pressure_local_hpa: float, temperature_local_c: float, relative_humidity_local_pct: float) -> float:

    if pressure_local_hpa <= 0 or pressure_sea_level_hpa <= 0:
        raise ValueError("Pressures must be positive.")
    if pressure_local_hpa > pressure_sea_level_hpa:
        pass
    tv_local_k = calculate_virtual_temperature(
        temperature_local_c, 
        relative_humidity_local_pct, 
        pressure_local_hpa
    )

    mean_tv_k = tv_local_k

    altitude = (RD * mean_tv_k / G0) * math.log(pressure_sea_level_hpa / pressure_local_hpa)
    
    return altitude
