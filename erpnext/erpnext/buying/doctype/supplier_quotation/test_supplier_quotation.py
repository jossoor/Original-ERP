# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import add_days, today


class TestPurchaseOrder(FrappeTestCase):
	def test_make_purchase_order(self):
		from erpnext.buying.doctype.supplier_quotation.supplier_quotation import make_purchase_order

		sq = frappe.copy_doc(test_records[0]).insert()

		self.assertRaises(frappe.ValidationError, make_purchase_order, sq.name)

		sq = frappe.get_doc("Supplier Quotation", sq.name)
		sq.submit()
		po = make_purchase_order(sq.name)

		self.assertEqual(po.doctype, "Purchase Order")
		self.assertEqual(len(po.get("items")), len(sq.get("items")))

		po.naming_series = "_T-Purchase Order-"

		for doc in po.get("items"):
			if doc.get("item_code"):
				doc.set("schedule_date", add_days(today(), 1))

		po.insert()


test_records = frappe.get_test_records("Supplier Quotation")
