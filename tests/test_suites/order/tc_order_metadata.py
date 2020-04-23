from tests.bases.base_test_case import BaseTestCase
from tests.helpers.time import epoch_time, time_in_past

class TC_OrderMetadata(BaseTestCase):
  def test_columns(self):
    query = f"""
      SHOW COLUMNS FROM `{self.report_db_name}`.order;
    """
    
    column_metadata_list = self.report_db_helper.find_all(query)
    
    columns_by_field = {
      column_meta_data['Field'] : column_meta_data
      for column_meta_data in column_metadata_list
    }

    self.assertDictContainsSubset({
      'Type': 'varchar(255)',
      'Null': 'NO',
      'Key': 'PRI'
    }, columns_by_field['id'])

    self.assertDictContainsSubset({
      'Type': 'bigint',
      'Null': 'NO',
    }, columns_by_field['created_order_time'])
   
    self.assertDictContainsSubset({
      'Type': 'varchar(255)',
      'Null': 'NO',
    }, columns_by_field['lead_id'])
  
  def test_contraints(self):
    query = f"""
      SELECT CONSTRAINT_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
      FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
      WHERE CONSTRAINT_SCHEMA = '{self.report_db_name}'
      AND TABLE_NAME = 'lead'
    """
    
    constraint_list = self.report_db_helper.find_all(query)

    contraint_list_by_native_column_name = {
      contraint['COLUMN_NAME']: contraint
      for contraint in constraint_list
    }

    self.assertDictContainsSubset({
      'CONSTRAINT_NAME': 'PRIMARY'
    }, contraint_list_by_native_column_name['id'])

    self.assertDictContainsSubset({
      'REFERENCED_TABLE_NAME': 'contact',
      'REFERENCED_COLUMN_NAME': 'id',
    }, contraint_list_by_native_column_name['contact_id'])

    self.assertDictContainsSubset({
      'REFERENCED_TABLE_NAME': 'salesman',
      'REFERENCED_COLUMN_NAME': 'id',
    }, contraint_list_by_native_column_name['salesman_username_id'])

    self.assertDictContainsSubset({
      'REFERENCED_TABLE_NAME': 'status',
      'REFERENCED_COLUMN_NAME': 'id',
    }, contraint_list_by_native_column_name['status_id'])

    self.assertDictContainsSubset({
      'REFERENCED_TABLE_NAME': 'content',
      'REFERENCED_COLUMN_NAME': 'id',
    }, contraint_list_by_native_column_name['content_id'])
