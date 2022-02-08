from flask import Blueprint, render_template, flash, url_for, redirect, request, session
from flask_login import login_required, current_user
from datetime import datetime

from database.database import get_db

bp = Blueprint('shifts', __name__, url_prefix='/shifts')


@bp.route('<record_id>/<object_type>/shifts', methods=['GET'])
def delete(record_id, object_type):
    db = get_db()

    try:
        if object_type == 'report':
            deleted_id = db.execute("DELETE FROM employeeOnShift WHERE id = ?", [record_id]).lastrowid
            db.commit()
            return redirect(url_for('shifts.report_list'))
        else:
            deleted_id = db.execute("DELETE FROM shift WHERE id = ?", [record_id]).lastrowid
            db.commit()
            return redirect(url_for('shifts.shift_list'))

    except db.Error as e:
        flash('There is some problem with database.', 'error')
        print('DB Error: ' + str(e))


@bp.route('<shift_id>/shifts/', methods=['GET'])
def delete_shift(shift_id):
    db = get_db()

    try:
        deleted_id = db.execute("DELETE FROM shift WHERE id = ?", [shift_id]).lastrowid
        db.commit()
    except db.Error as e:
        flash('There is some problem with database.', 'error')
        print('DB Error: ' + str(e))

    return redirect(url_for('shifts.shift_list'))


@bp.get('/')
@login_required
def shift_list():
    db = get_db()
    shifts = []

    try:
        if current_user.role == "partner":
            shifts = db.execute(
                "SELECT shift.id, partner.companyName, position.name, "
                "strftime('%d-%m-%Y %H:%M', datetime(startTime/1000, 'unixepoch')) sTime, "
                "strftime('%d-%m-%Y %H:%M', datetime(endTime/1000, 'unixepoch')) eTime, hourlyWage, currencyCode "
                "FROM shift "
                "INNER JOIN position ON shift.positionId = position.id "
                "INNER JOIN partner  ON position.partnerId = partner.id "
                "WHERE userId = ?", current_user.user_id
            ).fetchall()
        else:
            shifts = db.execute(
                "SELECT shift.id, partner.companyName, position.name, "
                "strftime('%d-%m-%Y %H:%M', datetime(startTime/1000, 'unixepoch')) sTime, "
                "strftime('%d-%m-%Y %H:%M', datetime(endTime/1000, 'unixepoch')) eTime, hourlyWage, currencyCode "
                "FROM shift "
                "INNER JOIN position ON shift.positionId = position.id "
                "INNER JOIN partner  ON position.partnerId = partner.id"
            ).fetchall()

    except db.Error as e:
        flash('There is some problem with database.', 'error')
        print('DB Error: ' + str(e))

    return render_template('shifts/shifts.html', shifts=shifts)


@bp.route('/report/<shift_id>', methods=['GET'])
def register(shift_id):
    db = get_db()

    try:
        shift_data = db.execute("SELECT id, "
                                "strftime('%d-%m-%Y %H:%M', datetime(startTime/1000, 'unixepoch')) sTime, "
                                "strftime('%d-%m-%Y %H:%M', datetime(endTime/1000, 'unixepoch')) eTime, "
                                "hourlyWage, currencyCode "
                                "FROM shift "
                                "WHERE id = ?", [shift_id]
                                ).fetchone()

        worked_hours = datetime.strptime(shift_data['eTime'], '%d-%m-%Y %H:%M').hour - datetime.strptime(
            shift_data['sTime'], '%d-%m-%Y %H:%M').hour
        shift_pay = worked_hours * shift_data['hourlyWage']

        new_id = db.execute("INSERT INTO employeeOnShift (shiftId, userId, shiftPay, workedHours, loggedIn) "
                            "VALUES (?, ?, ?, ?, ?)",
                            (shift_id, int(current_user.user_id), shift_pay, worked_hours, 1)).lastrowid
        db.commit()
    except db.Error as e:
        if str(e).__contains__("UNIQUE constraint"):
            flash("You are already registered for this position!", 'error')
        else:
            flash('There is some problem with database.', 'error')
            print('DB Error: ' + str(e))

    return redirect(url_for('shifts.report_list'))


@bp.get('/report')
def report_list():
    db = get_db()
    reports = []
    sum_worked_hours = 0
    sum_shift_pay = 0

    try:
        if current_user.role == "administrator":
            reports = db.execute(
                "SELECT employeeOnShift.id, position.name, position.description, partner.companyName, partner.sector, "
                "shiftPay, employeeOnShift.workedHours, shift.currencyCode, user.username "
                "FROM employeeOnShift INNER JOIN shift ON shiftid = shift.id "
                "INNER JOIN position ON position.id = shift.positionId "
                "INNER JOIN partner ON partner.id = position.partnerId "
                "INNER JOIN user ON user.id = employeeOnShift.userId"
            ).fetchall()
        else:
            reports = db.execute(
                "SELECT employeeOnShift.id, position.name, position.description, partner.companyName, partner.sector, "
                "shiftPay, employeeOnShift.workedHours, shift.currencyCode, user.username "
                "FROM employeeOnShift INNER JOIN shift ON shiftid = shift.id "
                "INNER JOIN position ON position.id = shift.positionId "
                "INNER JOIN partner ON partner.id = position.partnerId "
                "INNER JOIN user ON user.id = employeeOnShift.userId "
                "WHERE employeeOnShift.userId = ?", [int(current_user.user_id)]
            ).fetchall()

        for report in reports:
            sum_shift_pay += report['shiftPay']
            sum_worked_hours += report['workedHours']

    except db.Error as e:
        flash('There is some problem with database.', 'error')
        print('DB Error: ' + str(e))

    return render_template('shifts/report.html', reports=reports,
                           sum_shift_pay=sum_shift_pay,
                           sum_worked_hours=sum_worked_hours)


@bp.get('/creation')
def creation():
    db = get_db()
    positions = []

    if current_user.role == "employee":
        return render_template('403.html')

    try:
        positions = db.execute(
            "SELECT DISTINCT partnerId, partner.companyName "
            "FROM position "
            "INNER JOIN partner ON position.partnerId = partner.id"
        ).fetchall()

    except db.Error as e:
        flash('There is some problem with database.', 'error')
        print('DB Error: ' + str(e))

    return render_template('shifts/creation.html', positions=positions, data={})


@bp.route('/creation', methods=['GET', 'POST'])
def creation_nd():
    db = get_db()
    positions = []
    data = request.form

    session['startTime'] = data['startTime']
    session['endTime'] = data['endTime']

    if request.method == 'GET':
        return redirect(url_for('shifts.create'))

    if current_user.role == "employee":
        return render_template('403.html')

    try:
        positions = db.execute(
            "SELECT position.id, name "
            "FROM position "
            "INNER JOIN partner ON position.partnerId = partner.id "
            "WHERE partner.id == ?", [data['company']]
        ).fetchall()

    except db.Error as e:
        flash('There is some problem with database.', 'error')
        print('DB Error: ' + str(e))

    return render_template('shifts/creation_nd.html', positions=positions, data={})


@bp.post('/creation/second')
def create():
    db = get_db()
    data = request.form
    start_time = session.get('startTime', None)
    end_time = session.get('endTime', None)

    if current_user.role == "employee":
        return render_template('403.html')

    try:
        timestamp_start_time = (datetime.timestamp(datetime.strptime(start_time, '%Y-%m-%dT%H:%M')) * 1000)
        timestamp_end_time = (datetime.timestamp(datetime.strptime(end_time, '%Y-%m-%dT%H:%M')) * 1000)

        new_id = db.execute("INSERT INTO shift (positionId, startTime, endTime, hourlyWage, currencyCode) "
                            "VALUES (?, ?, ?, ?, ?)",
                            (data['position'], timestamp_start_time, timestamp_end_time, data['hourlyWage'],
                             data['currency'])).lastrowid
        db.commit()

    except db.Error as e:
        flash('There is some problem with database.', 'error')
        print('DB Error: ' + str(e))

    return redirect(url_for('shifts.shift_list'))


@bp.route('/')
def introduction():
    return render_template('shifts/shifts.html', show_header=True)
