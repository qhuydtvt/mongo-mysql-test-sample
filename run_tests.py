import unittest
# pylint: disable=unused-wildcard-import
from tests.test_suites.main import *
from tests.configs.main import Config

if __name__ == "__main__":
  Config.init('local')
  unittest.main()
