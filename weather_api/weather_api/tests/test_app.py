import unittest
from app import app, db, WeatherData, WeatherStations, StationYearlyStatistics

class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        with app.app_context():
            db.create_all()

            # Add test data
            station1 = WeatherStations(station_name="USC0011", state="Nebraska", row_key="key1")
            db.session.add(station1)
            db.session.commit()

            weather1 = WeatherData(date="2020-01-01", max_temp=350, min_temp=150, precipitation=20, station_id=station1.id, file_name="file1", row_key="key2")
            db.session.add(weather1)
            db.session.commit()

            stats1 = StationYearlyStatistics(station_name="USC0011", year=2020, avg_max_temp=35.0, avg_min_temp=15.0, total_precipitation=2.0, row_key="key3")
            db.session.add(stats1)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_get_weather_data(self):
        response = self.app.get('/api/weather')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json)

    def test_get_weather_stats(self):
        response = self.app.get('/api/weather/stats')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json)

if __name__ == '__main__':
    unittest.main()
