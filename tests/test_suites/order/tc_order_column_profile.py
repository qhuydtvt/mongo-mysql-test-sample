from tests.bases.base_test_case import BaseTestCase
from tests.helpers.time import epoch_time, time_in_past

class TC_OrderColumnProfile(BaseTestCase):
  def test_total_order_value(self):
    now = epoch_time()
    _1_last_month = epoch_time(time_in_past(4))

    app_aggregate = [
      {
        '$match': {
          'createdAt': {
            '$gte': _1_last_month * 1000,
            '$lte': now * 1000
          },
          'order.productItems': {
            '$exists': True
          }
        }
      },
      {
        '$project': {
          'productItem': '$order.productItems'
        }
      },
      {
        '$unwind': '$productItem'
      },
      {
        '$group': {
          '_id': None,
          'totalPriceBeforeDiscount': {
            '$sum': '$productItem.product.price'
          }
        }
      }
    ]

    print(now, _1_last_month)

    query = f"""SELECT SUM(tblOrderContactProduct.price_before_discount) AS totalPriceBeforeDiscount
                FROM {self.report_db_name}.lead as tblLead
                INNER JOIN {self.report_db_name}.order as tblOrder ON tblOrder.lead_id = tblLead.id
                INNER JOIN {self.report_db_name}.`order-contact-product` as tblOrderContactProduct ON tblOrderContactProduct.order_id = tblOrder.id
                WHERE
                tblLead.created_lead_time <= {now} AND
                tblLead.created_lead_time >= {_1_last_month};
    """

    app_order_total_price_before_discount = list(self.app_db['leads'].aggregate(app_aggregate))[0]['totalPriceBeforeDiscount']
    report_order_total_price_before_discount = int(self.report_db_helper.find_one(query)['totalPriceBeforeDiscount'])

    self.assertEqual(app_order_total_price_before_discount, report_order_total_price_before_discount)