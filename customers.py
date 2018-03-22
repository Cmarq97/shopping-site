"""Customers at Hackbright."""


class Customer(object):
    """Ubermelon customer."""

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __repr__(self):
        return "<Customer: {first}, {last}, {email}, {password}>".format(
            first=self.first_name, last=self.last_name, email=self.email,
            password=self.password)

# add get_by_email()


def read_customers_from_file(filepath):
    """Read customer data and populate dictionary of customers.

    Dictionary will be {id: email}
    """

    customers = {}

    for line in open(filepath):
        (first_name,
         last_name,
         email,
         password) = line.strip().split("|")

        customers[email] = Customer(first_name,
                                    last_name,
                                    email,
                                    password)

    return customers