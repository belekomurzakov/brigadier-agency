from flask import Blueprint, render_template, flash, url_for, request, redirect
from flask_login import login_required, current_user

from database.database import get_db

bp = Blueprint('companies', __name__, url_prefix='/companies')


@bp.route('<record_id>', methods=['GET'])
def delete(record_id):
    db = get_db()

    try:
        deleted_id = db.execute("DELETE FROM partner WHERE id = ?", [record_id]).lastrowid
        db.commit()
    except db.Error as e:
        flash('There is some problem with database.', 'error')
        print('DB Error: ' + str(e))

    return redirect(url_for('companies.partner_list'))


@bp.get('/')
@login_required
def partner_list():
    db = get_db()
    items = []

    try:
        if current_user.role == "partner":
            items = db.execute(
                "SELECT partner.id, companyName, sector, "
                "strftime('%d-%m-%Y', datetime(created/1000, 'unixepoch')) as_string, u.firstName "
                "FROM partner JOIN user u ON u.id = partner.userId "
                "WHERE userId = ?", current_user.user_id
            ).fetchall()
        else:
            items = db.execute(
                "SELECT partner.id, companyName, sector, "
                "strftime('%d-%m-%Y', datetime(created/1000, 'unixepoch')) as_string, u.firstName "
                "FROM partner JOIN user u ON u.id = partner.userId"
            ).fetchall()
    except db.Error as e:
        flash('There is some problem with database.', 'error')
        print('DB Error: ' + str(e))

    return render_template('companies/companies.html', items=items)


@bp.get('/creation')
def creation():
    if current_user.role == "employee":
        return render_template('403.html')

    return render_template('companies/creation.html', data={})


@bp.post('/creation')
def create():
    db = get_db()
    data = request.form

    try:
        new_id = db.execute("INSERT INTO partner (userid, companyName, sector)  VALUES (?, ?, ?)",
                            (int(current_user.user_id), data['companyName'], data['sector'])
                            ).lastrowid
        db.commit()
        print('New item id: ' + str(new_id))

    except db.Error as e:
        flash('There is some problem with database.', 'error')
        print('DB Error: ' + str(e))

    return redirect(url_for('companies.partner_list'))
