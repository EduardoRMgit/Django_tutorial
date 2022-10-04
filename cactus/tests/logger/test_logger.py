# -*- coding: utf-8 -*-
"""
These tests have the purpose of verifying the correct functioning of
DB LOGGER module.
"""

from django.test import TestCase


class LoggerTestCase(TestCase):

    def setUp(self):
        import logging
        from django.apps import apps

        # Our logger
        self.db_logger = logging.getLogger('db')

        # The model where messages are saved
        self.db_logger_model = apps.get_app_config(
            'CactusDBLogger').models.get('statuslog')

        # Messages to compare
        self.info_msg = "TEST info message"
        self.warning_msg = "Test warning message"

    def test_info(self):
        """Test for info message."""

        self.db_logger.info(self.info_msg)
        self.assertEqual(
            self.db_logger_model.objects.last().msg,
            self.info_msg
        )

    def test_warning(self):
        """Test for warning message."""

        self.db_logger.warning(self.warning_msg)
        self.assertEqual(
            self.db_logger_model.objects.last().msg,
            self.warning_msg
        )

    def test_exception(self):
        """Test for exception message."""

        ex_msg = ""
        try:
            420 / 0
        except Exception as ex:
            ex_msg = ex
            self.db_logger.exception(ex)

        self.assertEqual(
            self.db_logger_model.objects.last().msg,
            str(ex_msg)
        )
