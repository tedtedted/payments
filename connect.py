import os 
import random
import configparser
from string import ascii_uppercase
import json

from ingenico.connect.sdk.api_exception import ApiException
from ingenico.connect.sdk.declined_payment_exception import DeclinedPaymentException
from ingenico.connect.sdk.factory import Factory
from ingenico.connect.sdk.domain.definitions.address import Address
from ingenico.connect.sdk.domain.definitions.amount_of_money import AmountOfMoney
from ingenico.connect.sdk.domain.definitions.card import Card
from ingenico.connect.sdk.domain.payment.create_payment_request import CreatePaymentRequest
from ingenico.connect.sdk.domain.payment.definitions.card_payment_method_specific_input import CardPaymentMethodSpecificInput
from ingenico.connect.sdk.domain.payment.definitions.contact_details import ContactDetails
from ingenico.connect.sdk.domain.payment.definitions.customer import Customer
from ingenico.connect.sdk.domain.payment.definitions.line_item_invoice_data import LineItemInvoiceData
from ingenico.connect.sdk.domain.payment.definitions.order import Order
from ingenico.connect.sdk.domain.payment.definitions.order_references import OrderReferences
from ingenico.connect.sdk.domain.payment.definitions.personal_information import PersonalInformation
from ingenico.connect.sdk.domain.payment.definitions.personal_name import PersonalName

from fake import Person

config = configparser.RawConfigParser()
config.read('private.ini')

API_KEY_ID = config.get('CONNECT','API_KEY_ID')
SECRET_API_KEY = config.get('CONNECT','SECRET_API_KEY')
MERCHANT_ID = config.get('CONNECT','MERCHANT_ID')

class CreatePayment:

    def __init__(self):

        person = Person()

        self.customer_id = person.customer_id
        self.first_name = person.first_name
        self.last_name = person.last_name
        self.email_address = person.email
        self.phone_number = person.phone_number
        self.street = person.street
        self.zip = person.zip
        self.city = person.city
        self.country_code = person.country

        self.locale = person.locale_code

        self.currency_code = person.currency

        self.transaction_id = random.randint(10**8,10**9-1)
        self.merch_ref = ''.join(random.choice(ascii_uppercase) for _ in range(10))

    def example(self):
        with self.__get_client() as client:

            card = Card()
            card.card_number = "4567350000427977"
            card.cardholder_name = f'{self.first_name} {self.last_name}'
            card.cvv = "123"
            card.expiry_date = "1220"

            card_payment_method_specific_input = CardPaymentMethodSpecificInput()
            card_payment_method_specific_input.card = card
            card_payment_method_specific_input.payment_product_id = 1
            card_payment_method_specific_input.skip_authentication = True
            card_payment_method_specific_input.requres_approval = False

            amount_of_money = AmountOfMoney()
            amount_of_money.amount = random.randint(1,100) * 100
            amount_of_money.currency_code = self.currency_code

            billing_address = Address()
            billing_address.city = self.city
            billing_address.country_code = self.country_code
            billing_address.street = self.street
            billing_address.zip = self.zip

            contact_details = ContactDetails()
            contact_details.email_address = self.email_address
            contact_details.phone_number = self.phone_number

            name = PersonalName()
            name.first_name = self.first_name
            name.surname = self.last_name

            personal_information = PersonalInformation()
            personal_information.name = name

            customer = Customer()
            customer.billing_address = billing_address
            customer.contact_details = contact_details
            customer.locale = self.locale
            customer.merchant_customer_id = self.customer_id
            customer.personal_information = personal_information

            references = OrderReferences()
            references.merchant_order_id = self.transaction_id
            references.merchant_reference = self.merch_ref
            
            order = Order()
            order.amount_of_money = amount_of_money
            order.customer = customer
            order.references = references

            body = CreatePaymentRequest()
            body.card_payment_method_specific_input = card_payment_method_specific_input
            body.order = order

            try:
                response = client.merchant(MERCHANT_ID).payments().create(body)
                return json.dumps(response.payment.to_dictionary(),indent=2)

            except DeclinedPaymentException as e:
                self.handle_declined_payment(e.create_payment_result)
                print(e)

            except ApiException as e:
                self.handle_api_errors(e.errors)
                print(e)

    def __get_client(self):
        api_key_id = API_KEY_ID
        secret_api_key = SECRET_API_KEY
        configuration_file_name = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                               'configuration.ini'))
        return Factory.create_client_from_file(configuration_file_name=configuration_file_name,
                                               api_key_id=api_key_id, secret_api_key=secret_api_key)

    def handle_declined_payment(self, create_payment_result):
        # handle the result here
        pass

    def  handle_api_errors(self, errors):
        # handle the errors here
        pass

pay = CreatePayment()

r = pay.example()
print(r)
