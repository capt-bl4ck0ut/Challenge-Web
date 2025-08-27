from app.models import Report
from app.components import get_db


def get_reports():
    db = get_db()
    return db.session.execute(db.select(Report)).scalars().all()


def get_report(report_id):
    db = get_db()
    return db.session.execute(db.select(Report).where(Report.id == report_id)).scalars().first()


def add_report(post_id, reason, reporter_id):
    db = get_db()
    db.session.add(Report(post_id=post_id, reason=reason, reporter_id=reporter_id))
    db.session.commit()


def remove_report(report_id):
    db = get_db()
    db.session.execute(db.delete(Report).where(Report.id == report_id))
    db.session.commit()
