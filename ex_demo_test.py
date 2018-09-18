import unittest

def create_product(name, price):
    return {
        'name': name,
        'price': price,
    }

def create_invoice_line(product, quantity):
    return {
        'product': product,
        'quantity': quantity,
        'amount': quantity * product['price']
    }

def create_invoice(name, customer, invoice_lines, vat=1.21):
    # amount = 0.0
    # for line in invoice_lines:
    #     amount += line['amount']
    amount = sum(line['amount'] for line in invoice_lines)

    return {
        'name': name,
        'customer': customer,
        'amount': amount,
        'vat': vat,
        'total_amount': amount * vat
    }

# def create_customer(name):
#     return {
#         'name': name
#     }

class ProductTestCase(unittest.TestCase):
    def test_product_creation(self):
        product = create_product('iPhone', 1000.0)

        self.assertEqual(product['name'], 'iPhone')
        self.assertEqual(product['price'], 1000.0)

    def test_product_creation_name(self):
        with self.assertRaises(AssertionError):
            create_produit(12345678, 1.0)


if __name__ == '__main__':
    unittest.main()