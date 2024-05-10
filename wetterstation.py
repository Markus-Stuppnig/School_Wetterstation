import unittest
from unittest.mock import MagicMock
import random

class Reading:
    temperature: float = None
    pressure: float = None
    
    def __init__(self, temperature, pressure):
        self.temperature = temperature
        self.pressure = pressure


class Sensor:
    def get_reading(self):
        temperature = self._generate_temperature()
        pressure = self._generate_pressure()
        return Reading(temperature, pressure)
    
    def _generate_temperature(self):
        return random.uniform(-10, 40)

    def _generate_pressure(self):
        return random.uniform(900, 1100)


class Weatherstation:
    _MAX_READINGS: int = 10

    def __init__(self, sensor: Sensor):
        self._sensor = sensor
        self._readings = []

    def record_reading(self):
        new_reading: Reading = self._sensor.get_reading()
        if len(self._readings) >= self._MAX_READINGS:
            self._readings.pop(0)
        self._readings.append(new_reading)

    def avg_temperature(self):
        if not len(self._readings):
            raise ValueError("Es sind noch keine Readings vorhanden")

        temperature: float = 0
        for reading in self._readings:
            temperature += reading.temperature

        return temperature / len(self._readings)

    def avg_pressure(self):
        if not len(self._readings):
            raise ValueError("Es sind noch keine Readings vorhanden")

        pressure: float = 0
        for reading in self._readings:
            pressure += reading.pressure

        return pressure / len(self._readings)


class TestSensor(unittest.TestCase):
    def setUp(self):
        self.sensor = Sensor()

    def test_generate_temperature(self):
        temperature = self.sensor._generate_temperature()
        self.assertTrue(-10 <= temperature <= 40)

    def test_generate_pressure(self):
        pressure = self.sensor._generate_pressure()
        self.assertTrue(900 <= pressure <= 1100)

    def test_get_reading(self):
        reading = self.sensor.get_reading()
        self.assertIsInstance(reading, Reading)
        self.assertIsInstance(reading.temperature, float)
        self.assertIsInstance(reading.pressure, float)


class TestWeatherstation(unittest.TestCase):
    def setUp(self):
        self.sensor = Sensor()
        self.station = Weatherstation(self.sensor)

    def test_record_reading(self):
        initial_readings_count = len(self.station._readings)
        self.station.record_reading()
        self.assertEqual(len(self.station._readings), initial_readings_count + 1)

    def test_avg_temperature_empty_readings(self):
        with self.assertRaises(ValueError) as context:
            self.station.avg_temperature()
        self.assertEqual(str(context.exception), "Es sind noch keine Readings vorhanden")

    def test_avg_pressure_empty_readings(self):
        with self.assertRaises(ValueError) as context:
            self.station.avg_pressure()
        self.assertEqual(str(context.exception), "Es sind noch keine Readings vorhanden")

    def test_avg_temperature(self):
        for i in range(15):
            self.station.record_reading()
        self.assertAlmostEqual(self.station.avg_temperature(), 15, delta=25)

    def test_avg_pressure(self):
        for i in range(15):
            self.station.record_reading()
        self.assertAlmostEqual(self.station.avg_pressure(), 1000, delta=100)

if __name__ == '__main__':
    unittest.main()