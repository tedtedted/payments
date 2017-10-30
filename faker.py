import random

from faker import Faker
from faker import config
from babel import Locale
from babel import numbers
from babel import core


class Person():
    def __init__(self):

        self.locale_code = _return_locale()
        self.l = Locale.parse(self.locale_code)
        self.fake = Faker(self.locale_code)

        self.first_name = self.fake.first_name()
        self.last_name = self.fake.last_name()
        self.email = self.fake.email()
        self.street = self.fake.street_address()
        self.zip = self.fake.postcode()
        self.city = self.fake.city()
        self.country = self.l.territory
        self.currency = numbers.get_territory_currencies(self.country)[0]
        self.customer_id = random.randint(10**9,10**10-1)

    def __str__(self):
        return self.__dict__.items()


def _return_locale():
    faker_locales = set(config.AVAILABLE_LOCALES)
    babel_locales = set(core.LOCALE_ALIASES.values())

    available_locale = faker_locales.intersection(babel_locales)

    locale = random.choice(tuple(available_locale))

    return locale