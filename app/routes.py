from flask import Blueprint, render_template, request, redirect, url_for, current_app
import bleach


main = Blueprint('main', __name__)
from app.forms import *


@main.route('/', methods=['GET'])
def home():
    return redirect(url_for('main.register'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = Register()
    safeBio = ""
    client_ip = request.remote_addr
    if form.validate_on_submit():
        safeBio = bleach.clean(
            form.bio.data,
            tags=['b', 'i','u', 'a','em','strong','a','p','ul','ol','li'],  # No HTML tags allowed
            attributes={'a': ['href', 'title']},  # No attributes allowed
            strip=True  # Remove disallowed tags entirely
        )
        if form.bio.data != safeBio and form.bio.data.strip():  # .strip() avoids logging for just whitespace
            current_app.logger.warning(
                f"SUSPICIOUS INPUT (Sanitized) from IP **{client_ip}** for user **{form.username.data}**. "
                f"Original bio: **{form.bio.data}**"
            )

        current_app.logger.info(
            f"SUCCESSFUL registration for user **{form.username.data}** from IP **{client_ip}**"
        )
    else:
        error_details = "; ".join([f"{field}: {errors[0]}" for field, errors in form.errors.items()])
        if 'username' in form.errors:
            for error in form.errors['username']:
                if 'reserved' in error:  # Checks for the error message from your validator
                    current_app.logger.warning(
                        f"SUSPICIOUS INPUT from IP **{client_ip}**: Attempted reserved username **{form.username.data}**"
                    )
        current_app.logger.warning(
           f"VALIDATION FAILURE/SUSPICIOUS INPUT from IP **{client_ip}**. Errors: **{error_details}**"
        )


    return render_template('register.html', form = form,bio = safeBio,name = form.username.data)

