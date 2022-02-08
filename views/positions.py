from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_required, current_user

from database.database import get_db

bp = Blueprint('positions', __name__, url_prefix='/positions')


@bp.route('<record_id>', methods=['GET'])
def delete(record_id):
    db = get_db()

    try:
        id = db.execute("DELETE FROM position WHERE id = ?", [record_id]).lastrowid
        db.commit()
    except db.Error as e:
        flash('There is some problem with database.', 'error')
        print('DB Error: ' + str(e))

    return redirect(url_for('positions.position_list'))


@bp.get('/')
@login_required
def position_list():
    db = get_db()
    positions = []

    try:
        if current_user.role == "partner":
            positions = db.execute(
                "SELECT position.id, name, description, partner.companyName, partner.sector, "
                "user.firstName "
                "FROM position INNER JOIN partner ON position.partnerId = partner.id "
                "INNER JOIN user ON partner.userId = user.id "
                "WHERE userId = ?", current_user.user_id
            ).fetchall()
        else:
            positions = db.execute(
                "SELECT position.id, name, description, partner.companyName, partner.sector, "
                "user.firstName "
                "FROM position INNER JOIN partner ON position.partnerId = partner.id "
                "INNER JOIN user ON partner.userId = user.id"
            ).fetchall()
    except db.Error as e:
        flash('There is some problem with database.', 'error')
        print('DB Error: ' + str(e))

    return render_template('positions/positions.html', positions=positions)


@bp.get('/creation')
def creation():
    db = get_db()
    items = []

    if current_user.role == "employee":
        return render_template('403.html')

    try:
        items = db.execute(
            "SELECT id, companyName "
            "FROM partner"
        ).fetchall()
    except db.Error as e:
        flash('There is some problem with database.', 'error')
        print('DB Error: ' + str(e))

    return render_template('positions/creation.html', items=items, data={})


@bp.post('/creation')
def create():
    db = get_db()
    data = request.form

    try:
        partner_data = db.execute("SELECT id FROM partner WHERE companyName LIKE ?",
                                  ('%' + data['company'] + '%',)).fetchone()

        new_id = db.execute("INSERT INTO position (partnerId, name, description) "
                            "VALUES (?, ?, ?)",
                            (partner_data['id'], data['name'], data['description'])).lastrowid
        db.commit()
    except db.Error as e:
        flash('There is some problem with database.', 'error')
        print('DB Error: ' + str(e))

    return redirect(url_for('positions.position_list'))


@bp.route('/')
def introduction():
    return render_template('positions/positions.html', show_header=True)
