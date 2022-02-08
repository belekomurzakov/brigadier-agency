from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required

from database.database import get_db

bp = Blueprint('contacts', __name__, url_prefix='/contacts')


@bp.route('<record_id>', methods=['GET'])
def delete(record_id):
    db = get_db()

    try:
        deleted_id = db.execute("DELETE FROM user WHERE id = ?", [record_id]).lastrowid
        db.commit()
    except db.Error as e:
        flash('There is some problem with database.', 'error')
        print('DB Error: ' + str(e))

    return redirect(url_for('contacts.contact_list'))


@bp.get('/')
@login_required
def contact_list():
    db = get_db()
    contacts = []

    try:
        contacts = db.execute(
            "SELECT id, firstname, lastname, username, userrole, mobile, street, city, country, "
            "strftime('%d-%m-%Y', datetime(birthdate/1000, 'unixepoch')) birthdate_s "
            "FROM user"
        ).fetchall()
    except db.Error as e:
        flash('There is some problem with database.', 'error')
        print('DB Error: ' + str(e))

    return render_template('contact/contact.html', contacts=contacts)


@bp.route('/')
def introduction():
    return render_template('contact/contact.html', show_header=True)
