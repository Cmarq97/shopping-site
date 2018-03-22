"""Customers at Hackbright."""


class Customer(object):
    """Ubermelon customer."""

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hash_password = hash(password)

    def __repr__(self):
        return "<Customer: {first}, {last}, {email}, {password}>".format(
            first=self.first_name, last=self.last_name, email=self.email,
            password=self.hash_password)

    def is_correct_password(self, password):
        return hash(password) == self.hash_password


def read_customers_from_file(filepath):
    """Read customer data and populate dictionary of customers.

    Dictionary will be {email: Customer}
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


def get_by_email(email):
    """Return a customer, given their email, or None if email doesn't exist."""

    # This relies on access to the global dictionary `customers`

    return customers.get(email, None)


customers = read_customers_from_file("customers.txt")
