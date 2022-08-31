# -*- coding: utf-8 -*-
"""
These tests have the purpose of verifying the correct functioning of
Location and Device logger
"""

from ..common import CactusGraphQLTestCase
from demograficos.models import GeoDevice, GeoLocation


class TestGeoLocation(CactusGraphQLTestCase):

    def test_localization_with_headers(self):

        device_id_header = "420"
        location_lat_header = 421.0
        location_lon_header = 422.0
        query = """
        query {
            allGeodevices{
                uuid
            }
        }
        """
        expected_res = {
            "allGeodevices":
            [
                {
                    "uuid": "420"
                }
            ]
        }
        response = self.query(query,
                              device_id_header=device_id_header,
                              location_lat_header=location_lat_header,
                              location_lon_header=location_lon_header,
                              username_header=self._username)
        self.assertResponse(response, expected_res)

        # Check last insertion in DB
        self.assertEqual(location_lat_header, GeoLocation.objects.last().lat)
        self.assertEqual(location_lon_header, GeoLocation.objects.last().lon)
        self.assertEqual(device_id_header, GeoDevice.objects.last().uuid)

    def test_localization_without_headers(self):

        query = """
        query {
            allGeodevices{
                uuid
            }
        }
        """
        expected_res = {
            "allGeodevices": []
        }
        response = self.query(query)
        self.assertResponse(response, expected_res)

        # Check last insertion in DB (empty)
        self.assertEqual(0, GeoLocation.objects.count())
        self.assertEqual(0, GeoDevice.objects.count())
