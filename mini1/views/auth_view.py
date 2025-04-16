from flask import Blueprint
from flask import render_template,redirect, url_for
from flask import request, session

from werkzeug.security import generate_password_hash, check_password_hash

from ..db import memeber_util
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Handle login here (authentication logic)
        return "Logged in"
    return render_template("auth/login.html")  