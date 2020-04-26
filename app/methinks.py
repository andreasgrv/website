import datetime
from flask import Blueprint, request
from methinks.db import db, Entry
from methinks.utils import str_to_date
from app.utils import response, validate_post, validate_get


methinks_routes = Blueprint('methinks_routes', __name__)


@methinks_routes.route('/')
def root():
    return ''


@methinks_routes.route('/entries/<date>')
def get_entry(date):
    try:
        validate_get(request)
        if date == 'latest':
            entry = Entry.query.order_by(Entry.date.desc()).first()
        else:
            d = Entry.string_to_date(date)
            entry = Entry.query.filter_by(date=d).first()
        entry = {} if not entry else entry.as_dict()
        return response(True, 'OK', data=entry)
    except Exception as e:
        return response(False, msg=repr(e))


@methinks_routes.route('/entries/create', methods=['POST'])
def create_entry():
    try:
        data = dict(validate_post(request))
        text = data.pop('text')
        dt = data.pop('date')
        dt = str_to_date(dt)
        entry = Entry(text=text, date=dt.date(), **data)
        db.session.add(entry)
        db.session.commit()
        return response(True, 'OK', data=entry.as_dict())
    except Exception as e:
        return response(False, msg=repr(e))


@methinks_routes.route('/entries/update', methods=['POST'])
def update_entry():
    try:
        data = dict(validate_post(request))
        text = data.pop('text')
        dt = data.pop('date')
        dt = str_to_date(dt)
        entry = Entry.query.filter_by(date=dt.date()).first()
        if entry is None:
            raise ValueError("Failed to update entry.")
        entry.text = text
        entry.misc = data
        entry.last_edited = datetime.datetime.now()
        db.session.add(entry)
        db.session.commit()
        return response(True, 'OK', data=entry.as_dict())
    except Exception as e:
        return response(False, msg=repr(e))


@methinks_routes.route('/entries/delete', methods=['POST'])
def delete_entry():
    try:
        data = dict(validate_post(request))
        dt = str_to_date(data['date'])
        entry = Entry.query.filter_by(date=dt.date()).first()
        if entry:
            db.session.delete(entry)
            db.session.commit()
        return response(True, 'OK')
    except Exception as e:
        return response(False, msg=repr(e))
    return response(200, 'OK')
