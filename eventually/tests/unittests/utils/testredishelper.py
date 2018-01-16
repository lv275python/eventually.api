from django.test import TestCase
from utils.redishelper import REDIS_HELPER

class RedisHelperTestCase(TestCase):
    """TestCase for providing redishelper util testing."""

    def test_success_set_redis_worker(self):
        key = "my_key"
        value = "my_value"
        self.assertTrue(REDIS_HELPER.set(key, value))

    def test_success_get_redis_worker(self):
        key = "my_key"
        value = "my_value"
        REDIS_HELPER.set(key, value)
        self.assertEqual(REDIS_HELPER.get(key), value.encode())
