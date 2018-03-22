"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""

from flask import Flask, request, render_template, redirect, flash, session
#from flask_debugtoolbar import DebugToolbarExtension
import jinja2

import melons
import customers

app = Flask(__name__)

# A secret key is needed to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    print melon
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def show_shopping_cart():
    """Display conte # - check if a "cart" exists in the session, and create one (an empty
    #   dictionary keyed to the string "cart") if notnt of shopping cart."""

    melon_list = []
    order_total = 0
    if "cart" in session:
        cart = session["cart"]
        for melon_id, qty in cart.items():
            melon = melons.get_by_id(melon_id)
            melon.qty = qty
            melon.total = melon.price * qty
            order_total = order_total + melon.total
            melon_list.append(melon)
    else:
        flash("Your cart is empty!")

    return render_template("cart.html", melons=melon_list, order_total=order_total)


@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""

    cart = session.setdefault("cart", {})
    cart[melon_id] = cart.get(melon_id, 0) + 1
    flash("{} was successfully added to your cart!".format(
        melons.get_by_id(melon_id).common_name))
    return redirect("/cart")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    email = request.form.get("email")
    password = request.form.get("password")

    customer = customers.get_by_email(email)
    if customer is not None:
        if customer.is_correct_password(password):
            session["email"] = email
            flash("Login Successful!")
            return redirect("/melons")
        else:
            flash("Incorrect Password")
            return redirect("/login")
    else:
        flash("User Does Not Exist")
        return redirect("/login")


@app.route("/logout")
def process_logout():
    """ Logs user out of site."""

    del session["email"]
    flash("Logout Successful")

    return redirect("/melons")


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


@app.errorhandler(404)
def page_not_found(e):
    flash("404 Error: Melon not found!")
    return render_template('404.html'), 404

if __name__ == "__main__":
#     app.debug = True
#     DebugToolbarExtension(app)
    app.run()
