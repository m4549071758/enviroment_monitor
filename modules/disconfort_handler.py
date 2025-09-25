def disconfort_calculate(temp: float, humidity: float)-> float:
    disc_value = 0.81 * temp + 0.01 * humidity * (0.99 * temp - 14.3) + 46.3
    return disc_value