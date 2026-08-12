

class Convertor:

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self):
        if not self._initialized:
            self.rates_to_usd = {
                "USD": 1.0,
                "EUR": 1.09,
                "JPY": 0.0067,
                "GBP": 1.27,
                "CNY": 0.14,
                "CHF": 1.13,
                "CAD": 0.74
            }
            self._initialized = True


    def convert(self, amount, from_currency, to_currency):
        if from_currency not in self.rates_to_usd or to_currency not in self.rates_to_usd:
            raise ValueError("Unsupported currency for conversion.")
        amount_in_usd = float(amount) * self.rates_to_usd[from_currency]
        return round(amount_in_usd / self.rates_to_usd[to_currency], 2)




class Currency:

    def __init__(self, amount, denom="USD"):
        self.amount = float(amount)
        self.denomination = denom.upper()
        self.helper = Convertor()


    def __str__(self):
        return f"Currency worth {self.amount} {self.denomination}"


    def __repr__(self):
        return f"Currency({self.amount}, {self.denomination})"


    def getAmount(self, amt):
        if isinstance(amt, Currency):
            if self.denomination == amt.denomination:
                return amt.amount
            return self.helper.convert(amt.amount, amt.denomination, self.denomination)
        return float(amt)


    def __add__(self, amt):
        self.amount += self.getAmount(amt)
        return self


    def __iadd__(self, amt):
        return self.__add__(amt)


    def __sub__(self, amt):
        amountToSubtract = self.getAmount(amt)
        if amountToSubtract > self.amount:
            raise ValueError("Cannot subtract more than currency value.")
        self.amount -= amountToSubtract
        return self


    def __isub__(self, amt):
        return self.__sub__(amt)


    def __mul__(self, scalar):
        self.amount *= float(scalar)
        return self


    def __imul__(self, scalar):
        return self.__mul__(scalar)


    def __truediv__(self, dividend):
        if float(dividend) == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        self.amount /= float(dividend)
        return self


    def __itruediv__(self, dividend):
        return self.__truediv__(dividend)


    def __floordiv__(self, dividend):
        if float(dividend) == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        self.amount //= float(dividend)
        return self


    def __ifloordiv__(self, dividend):
        return self.__floordiv__(dividend)


    def __round__(self, ndigits=0):
        self.amount = round(self.amount, ndigits)
        return self


    def __eq__(self, other):
        try:
            return self.amount == self.getAmount(other)
        except (TypeError, ValueError):
            return False


    def __lt__(self, other):
        return self.amount < self.getAmount(other)


    def __gt__(self, other):
        return self.amount > self.getAmount(other)


    def __le__(self, other):
        return self.amount <= self.getAmount(other)


    def __ge__(self, other):
        return self.amount >= self.getAmount(other)


    def set_amount(self, amt):
        self.amount = float(amt)


    def convert(self, new_denom):
        newDenom = new_denom.upper()
        self.amount = self.helper.convert(self.amount, self.denomination, newDenom)
        self.denomination = newDenom

