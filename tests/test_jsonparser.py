#!/usr/bin/env python

"""
Test case for jsonparser.py module
"""

import unittest
from json_test_responses import OBSERVATION_JSON, OBSERVATION_NOT_FOUND_JSON, \
    SEARCH_RESULTS_JSON, INTERNAL_SERVER_ERROR_JSON, SEARCH_WITH_NO_RESULTS_JSON, \
    FORECAST_NOT_FOUND_JSON, THREE_HOURS_FORECAST_JSON
from pyowm.utils import jsonparser
from pyowm.exceptions.parse_response_exception import ParseResponseException
from pyowm.location import Location


class Test(unittest.TestCase):

    __bad_json = '{"a": "test", "b": 1.234, "c": [ "hello", "world"] }'
    
    def test_build_location_from(self):
        dict1 = { "coord": { "lon": -0.12574, "lat": 51.50853 }, "id": 2643743,
                  "name": u"London", "cnt": 9 }
        dict2 = { "city" : { "coord" : { "lat" : 51.50853, "lon" : -0.125739 }, 
                  "country" : "GB", "id" : 2643743, "name" : u"London",
                  "population" : 1000000 }
                 }
        result1 = jsonparser.build_location_from(dict1)
        result2 = jsonparser.build_location_from(dict2)
        self.assertTrue(isinstance(result1, Location))
        self.assertTrue(isinstance(result2, Location))
        self.assertNotIn(None, result1.__dict__.values(), "")
        self.assertNotIn(None, result2.__dict__.values(), "")

    def test_parse_observation(self):
        """
        Test that method returns a valid Observation object when provided
        with well-formed JSON data
        """
        result = jsonparser.parse_observation(OBSERVATION_JSON)
        self.assertFalse(result is None, "")
        self.assertFalse(result.get_reception_time() is None, "")
        self.assertFalse(result.get_location() is None, "")
        self.assertNotIn(None, result.get_location().__dict__.values(), "")
        self.assertFalse(result.get_weather() is None, "")
        self.assertNotIn(None, result.get_weather().__dict__.values(), "")
        
    def test_parse_observation_fails_with_malformed_JSON_data(self):
        """
        Test that method throws a ParseResponseException when provided with bad
        JSON data
        """
        self.assertRaises(ParseResponseException, jsonparser.parse_observation, self.__bad_json)
        
    def test_parse_observation_when_server_error(self):
        """
        Test that method returns None when server responds with an error JSON message
        """
        result = jsonparser.parse_observation(OBSERVATION_NOT_FOUND_JSON)
        self.assertTrue(result is None, "")
        
    def test_parse_search_results(self):
        """
        Test that method returns a list of valid Observation objects when provided
        with well-formed JSON data
        """
        result = jsonparser.parse_search_results(SEARCH_RESULTS_JSON)
        self.assertFalse(result is None, "")
        self.assertTrue(isinstance(result, list))
        for item in result:
            self.assertFalse(item is None, "")
            self.assertFalse(item.get_reception_time() is None, "")
            self.assertFalse(item.get_location() is None, "")
            self.assertNotIn(None, item.get_location().__dict__.values(), "")
            self.assertFalse(item.get_weather() is None, "")
            self.assertNotIn(None, item.get_weather().__dict__.values(), "")
        
    def test_parse_search_results_with_malformed_JSON_data(self):
        """
        Test that method throws a ParseResponseException when provided with bad
        JSON data
        """
        self.assertRaises(ParseResponseException, jsonparser.parse_search_results, self.__bad_json)
        
    def test_parse_search_results_when_no_results(self):
        """
        Test that method returns an empty list when server found no results
        """
        result = jsonparser.parse_search_results(SEARCH_WITH_NO_RESULTS_JSON)
        self.assertTrue(isinstance(result, list))
        self.assertEqual(0, len(result), "")
        
    def test_parse_search_results_when_server_error(self):
        """
        Test that method returns None when server responds with an 
        error JSON message
        """
        result = jsonparser.parse_search_results(INTERNAL_SERVER_ERROR_JSON)
        self.assertFalse(result, "")

    #def test_parse_forecast(self):
    #    """
    #    Test that method returns a valid Forecast object when provided
    #    with well-formed JSON data
    #    """
    #    result = jsonparser.parse_forecast(THREE_HOURS_FORECAST_JSON)
    #    self.assertTrue(result, "")
    #    self.assertTrue(result.get_reception_time(),"")
    #    self.assertTrue(result.get_interval(),"")
    #    self.assertTrue(result.get_location())
    #    self.assertNotIn(None, result.get_location().__dict__.values(), "")
    #    self.assertTrue(isinstance(result.get_weathers(),list), "")
    #    for weather in result:
    #        self.assertTrue(weather)
    #        self.assertNotIn(None, result.get_weather().__dict__.values(), "")
        
    def test_parse_forecast_with_malformed_JSON_data(self):
        """
        Test that method throws a ParseResponseException when provided with bad
        JSON data
        """
        self.assertRaises(ParseResponseException, jsonparser.parse_forecast, self.__bad_json)
        
    def test_parse_forecast_when_no_results(self):
        result = jsonparser.parse_forecast(FORECAST_NOT_FOUND_JSON)
        self.assertFalse(result is None)
        self.assertEqual(0, len(result), "")
        
    def test_parse_forecast_when_server_error(self):
        """
        Test that method returns None when server responds with an 
        error JSON message
        """
        result = jsonparser.parse_forecast(INTERNAL_SERVER_ERROR_JSON)
        self.assertFalse(result, "")

if __name__ == "__main__":
    unittest.main()