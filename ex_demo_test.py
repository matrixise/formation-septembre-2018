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


def create_invoice_line(product, quantity):
    return {
        'product': product,
        'quantity': quantity,
        'amount': quantity * product['price']
    }


def create_invoice(name, customer, invoice_lines, vat=1.21):
    amount = sum(line['amount'] for line in invoice_lines)

    return {
        'name': name,
        'customer': customer,
        'amount': amount,
        'vat': vat,
        'total_amount': amount * vat
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


if __name__ == '__main__':
    unittest.main()
