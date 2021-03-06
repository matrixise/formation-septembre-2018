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


class InvoiceLine:
    def __init__(self, product, quantity):
        self.product = product
        self._quantity = quantity

    @property
    def amount(self):
        return self.quantity * self.product.price

    def get_quantity(self):
        return self._quantity

    def set_quantity(self, value: float):
        assert isinstance(value, float) and value > 0.0
        self._quantity = value

    quantity = property(get_quantity, set_quantity)


def create_invoice_line(product, quantity):
    return InvoiceLine(product, quantity)


@dataclass
class Invoice:
    name: str
    customer: str
    vat: float
    invoice_lines: list

    @property
    def amount(self):
        return sum(line.amount for line in self.invoice_lines)


def create_invoice(name, customer, invoice_lines, vat=1.21):
    return Invoice(
        name=name,
        customer=customer,
        invoice_lines=invoice_lines,
        vat=vat
    )


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


class InvoiceLineTestCase(unittest.TestCase):
    def setUp(self):
        self.product = create_product('iPhone', 1000.0)

    def test_amount_invoice_line(self):
        invoice_line = create_invoice_line(self.product, 2.0)

        amount = self.product.price * 2.0
        self.assertEqual(amount, invoice_line.amount)

    def test_amount_invoice_change_quantity(self):
        invoice_line = create_invoice_line(self.product, 2.0)

        invoice_line.quantity = 10.0
        self.assertEqual(invoice_line.quantity, 10.0)

        with self.assertRaises(AssertionError):
            invoice_line.quantity = -1


class InvoiceTestCase(unittest.TestCase):
    def setUp(self):
        product = create_product('iPhone', 1000.0)
        invoice_line = create_invoice_line(product, 2.0)
        self.invoice = create_invoice('INV-2018/0001', 'Manfred', [invoice_line], vat=1.20)

    def test_invoice_check_name(self):
        self.assertTrue(self.invoice.name.startswith('INV-2018/'))

    def test_invoice_check_number_of_lines(self):
        self.assertEqual(len(self.invoice.invoice_lines), 1)

    def test_invoice_check_amount_functional(self):
        amount = sum(map(operator.attrgetter('amount'), self.invoice.invoice_lines))
        self.assertEqual(self.invoice.amount, amount)

    def test_invoice_check_amount_with_list_comprehension(self):
        amount = sum(line.amount for line in self.invoice.invoice_lines)
        self.assertEqual(self.invoice.amount, amount)

    def test_invoice_check_amount_with_for_loop(self):
        amount = 0
        for line in self.invoice.invoice_lines:
            amount = amount + line.amount
        self.assertEqual(self.invoice.amount, amount)


if __name__ == '__main__':
    unittest.main()
