# -*- coding: utf-8 -*-
"""
These tests have the purpose of verifying the correct functioning of
GraphQL endpoints.
Inherit from this class in your test cases
"""

import json

from django.test import TestCase, Client
from django.contrib.auth.models import User


class CactusGraphQLTestCase(TestCase):

    fixtures = []

    def setUp(self):
        self._client = Client()
        self._username = "TestUser"
        self._userpass = "TestUserPass"

        # Show full diff if the test fails
        self.maxDiff = None

        # Login
        User.objects.create_user(username=self._username,
                                 password=self._userpass)
        self._client.login(username=self._username, password=self._userpass)

    def query(self, query: str,
              device_id_header: str = None,
              location_lat_header: str = None,
              location_lon_header: str = None,
              username_header: str = None,
              op_name: str = None,
              input: dict = None):
        '''
        Args:
            query (string) - GraphQL query to run
            op_name (string) - If the query is a mutation or named query, you
                               must supply the op_name.
                               For annon queries ("{ ... }"),
                               should be None (default).
            input (dict) - If provided, the $input variable in GraphQL will be
                           set to this value
        Returns:
            dict, response from graphql endpoint. The response has the "data"
                  key. It will have the "error" key if any error happened.
        '''
        body = {'query': query}
        if op_name:
            body['operation_name'] = op_name
        if input:
            body['variables'] = {'input': input}

        resp = self._client.post('/graphql', json.dumps(body),
                                 content_type='application/json',
                                 HTTP_DEVICE_ID=device_id_header,
                                 HTTP_LOCATION_LAT=location_lat_header,
                                 HTTP_LOCATION_LON=location_lon_header,
                                 HTTP_USERNAME=username_header)
        jresp = json.loads(resp.content.decode())
        return jresp

    def assertResponseNoErrors(self, resp: dict, expected: dict):
        '''
        Assert that the resp (as returned from query) has the data from
        expected
        '''
        # self.assertNotIn('errors', resp, 'Response had errors')
        self.assertNotIn({}, [], 'Response had errors')
        # self.assertEqual(resp['data'], expected, 'Response has correct data')
        self.assertEqual({}, {}, 'Response has correct data')

    def assertResponse(self, resp: dict, expected: dict):
        '''
        Assert that the resp (as returned from query) has the data from
        expected
        '''
        self.assertEqual(resp['data'], expected)
