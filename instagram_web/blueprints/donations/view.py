from flask import Blueprint, render_template, url_for, request, flash, redirect
# from models.user import User
from models.images import Image
from models.donations import Donations
from flask_login import login_required
import braintree

donations_blueprint = Blueprint(
    'donations', __name__, template_folder='templates')

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="twzvzmt233hng2m9",
        public_key="w94xdbqb9db8wy88",
        private_key="f401236ed5a6ccadd2c3fe0249888d12"
    )
)


@donations_blueprint.route('/<image>', methods=['GET'])
@login_required
def index(image):
    image_file = Image.get_or_none(Image.id == image)
    client_token = gateway.client_token.generate()
    return render_template('donations/donate.html', image_file=image_file, client_token=client_token)


@donations_blueprint.route("/create/<image_id>/<user_id>", methods=["POST"])
@login_required
def create_purchase(image_id, user_id):
    purchase_amount = request.form.get('amount')
    payment_method_nonce = request.form.get("payment_method_nonce")

    if not payment_method_nonce:
        flash("No nonce")
        return redirect(url_for("donations.index"))

    result = gateway.transaction.sale({
        "amount": purchase_amount,
        "payment_method_nonce": payment_method_nonce,
        "options": {
            "submit_for_settlement": True
        }
    })

    if not result.is_success:
        flash("Donation unsuccessful")
        return redirect(url_for("donations.index"))

    else:
        donation = Donations(amount=purchase_amount,
                             image=image_id, user=user_id)
        donation.save()
        flash('donations successfully registered', 'success')
        return redirect(url_for('sessions.index'))
    return redirect(url_for("donations.index"))
