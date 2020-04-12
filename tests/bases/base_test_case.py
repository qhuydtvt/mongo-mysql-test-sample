from unittest import TestCase
from pymongo import MongoClient
import pymysql
from tests.configs.main import Config

from tests.helpers.mysql import MySQLHelper

class BaseTestCase(TestCase):
  def setUp(self):
    # Getting config
    config = Config.value
    # Get App and Report DB
    app_db_config = config['app_db']
    report_db_config = config['report_db']
    # Open connection
    self.app_db_conn = MongoClient(app_db_config['host'], app_db_config['port'])
    self.app_db = self.app_db_conn[app_db_config['db_name']]
    
    self.report_db_name = report_db_config['db_name']
    self.report_db_conn = pymysql.connect(host=report_db_config['host'],
                            user=report_db_config['credentials']['username'],
                            password=report_db_config['credentials']['password'],
                            db=report_db_config['db_name'],
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
    self.report_db_helper = MySQLHelper(self.report_db_conn)
  
  def tearDown(self):
    self.app_db_conn.close()
    self.report_db_conn.close()