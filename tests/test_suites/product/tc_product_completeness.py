from tests.bases.base_test_case import BaseTestCase
from tests.helpers.time import epoch_time, time_in_past

class TC_ProductCompleteness(BaseTestCase):
  def test_entire_data(self):
    query = f"""
      SELECT * FROM {self.report_db_name}.product
    """
    print(query)
    app_products = list(self.app_db['products'].find())
    report_products = self.report_db_helper.find_all(query)

    tested_app_products = {
      str(app_product['_id']): app_product['name']
      for app_product in app_products
    }

    tested_report_products = {
      str(report_product['id']): report_product['name']
      for report_product in report_products
    }
    
    self.assertEqual(len(app_products), len(report_products))

    self.assertEqual(tested_app_products, tested_report_products)
