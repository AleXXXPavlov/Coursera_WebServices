import requests
from decimal import Decimal
from main import convert


correct = Decimal('30417.4739')
result = convert(Decimal("1000.1000"), 'EUR', 'UAH', "17/02/2005", requests)
if result == correct:
    print("Correct")
else:
    print("Incorrect: %s != %s" % (result, correct))
