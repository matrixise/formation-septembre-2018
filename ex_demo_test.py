import operator
import unittest
from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float


def create_product(name, price):
    assert isinstance(name, str) and len(name.strip()) > 0
    assert isinstance(price, float) and price > 0.0
    return Product(name, price)


@dataclass
class InvoiceLine:
    product: Product
    quantity: float

    @property
    def amount(self):
        return self.quantity * self.product.price


def create_invoice_line(product, quantity):
    return InvoiceLine(product, quantity)


def create_invoice(name, customer, invoice_lines, vat=1.21):
    amount = sum(line.amount for line in invoice_lines)

    return {
        'name': name,
        'customer': customer,
        'amount': amount,
        'vat': vat,
        'total_amount': amount * vat,
        'invoice_lines': invoice_lines,
    }


class ProductTestCase(unittest.TestCase):
    def test_product_creation(self):
        product = create_product('iPhone', 1000.0)

        self.assertEqual(product.name, 'iPhone')
        self.assertEqual(product.price, 1000.0)

    def test_product_creation_name(self):
        with self.assertRaises(AssertionError):
            create_product(123, 1.0)

    def test_product_raise_exception_if_name_empty(self):
        with self.assertRaises(AssertionError):
            create_product('', 1.0)

        with self.assertRaises(AssertionError):
            create_product('                        ', 1.0)

    def test_amount_invoice_line(self):
        product = create_product('iPhone', 1000.0)
        invoice_line = create_invoice_line(product, 2.0)

        amount = product.price * 2.0
        self.assertEqual(amount, invoice_line.amount)

    def test_invoice(self):
        product = create_product('iPhone', 1000.0)
        invoice_line = create_invoice_line(product, 2.0)
        invoice = create_invoice('INV-2018/0001', 'Manfred', [invoice_line], vat=1.20)

        self.assertTrue(invoice['name'].startswith('INV-2018/'))
        self.assertEqual(len(invoice['invoice_lines']), 1)

        # amount = sum(map(operator.attrgetter('amount'), invoice['invoice_lines']))
        # self.assertEqual(invoice['amount'], amount)

        amount = sum(line.amount for line in invoice['invoice_lines'])
        self.assertEqual(invoice['amount'], amount)

        # amount = 0
        # for line in invoice['invoice_lines']:
        #     amount = amount + line.amount
        # self.assertEqual(invoice['amount'], amount)

if __name__ == '__main__':
    unittest.main()
