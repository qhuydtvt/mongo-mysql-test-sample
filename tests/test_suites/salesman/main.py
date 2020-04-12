from tests.bases.base_test_case import BaseTestCase

class TC_Salesman(BaseTestCase):
  def test_total(self):
    report_query = "SELECT COUNT(id) FROM salesman"
    app_aggregate = [{
      '$lookup': {
        'from': 'centres',
        'localField': 'centreId',
        'foreignField': '_id',
        'as': 'centre'
      }
    }, {
      '$unwind': '$centre'
    }, {
      '$match': {
        'centre._id': {
          '$exists': True
        }
      }
    }, {
      '$count': 'salesmanCount'
    }]
    
    report_salesman_count = self.report_db_helper.find_one(report_query)['COUNT(id)']
    app_salesman_count = list(self.app_db['users'].aggregate(app_aggregate))[0]['salesmanCount']

    self.assertEqual(app_salesman_count, report_salesman_count)
  
  def test_sample(self):
    report_query = """SELECT * FROM salesman
      ORDER BY RAND()
      LIMIT 1;"""
    
    report_random_salesman = self.report_db_helper.find_one(report_query)
    salesman_id = report_random_salesman['id']
    
    app_query = { '_id': salesman_id }
    
    app_random_salesman = self.app_db['users'].find_one(app_query)
    
    self.assertEqual(report_random_salesman['id'], app_random_salesman['_id'])
    self.assertEqual(report_random_salesman['username'], app_random_salesman['email'])
    self.assertEqual(report_random_salesman['name'], app_random_salesman['fullName'])
    self.assertEqual(bool(report_random_salesman['is_active']), app_random_salesman['isActive'])