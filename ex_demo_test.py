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

def test():
    product = create_product('iPhone', 1429.0)
    assert product['name'] == 'iPhone'
    assert product['price'] == 1429.0

    invoice_line = create_invoice_line(product, 10)
    assert invoice_line['product'] == product
    assert invoice_line['quantity'] == 10
    assert invoice_line['amount'] == 10 * product['price']

    invoice = create_invoice('INV-2018/0001', 'Stephane', [invoice_line])
    assert invoice['name'] == 'INV-2018/0001'
    assert invoice['amount'] == invoice_line['amount']
    assert invoice['total_amount'] == invoice['amount'] * 1.21

if __name__ == '__main__':
    test()




















