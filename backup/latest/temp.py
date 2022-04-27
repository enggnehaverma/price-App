from forex_python.converter import CurrencyRates

currency = CurrencyRates()

print(currency.get_rate('INR', 'EUR'))
