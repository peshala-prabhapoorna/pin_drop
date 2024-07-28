import datetime
from fastapi import FastAPI
import sys

# add 'database' folder to the system path
sys.path.insert(0, "database")
import connect

from utilities import Report, rows_to_reports

app = FastAPI()

# connect to PostgreSQL server
db_connection = connect.connect()
db_cursor = db_connection.cursor()


@app.get("/api/v0/")
async def root():
    return {"message": "this is pin-drop"}


@app.post("/api/v0/post/")
async def create_report(report: Report):
    sql = (
        "INSERT INTO reports(timestamp, title, location, directions, "
        "description, up_votes, down_votes)"
        "VALUES(%s, %s, %s, %s, %s, %s, %s)"
        "RETURNING *;"
    )

    values = (
        report.timestamp,
        report.title,
        report.location,
        report.directions,
        report.description,
        report.up_votes,
        report.down_votes,
    )

    db_cursor.execute(sql, values)
    entry = db_cursor.fetchone()
    db_connection.commit()

    new_report = Report(
        id=entry[0],
        timestamp=entry[1],
        title=entry[2],
        location=entry[3],
        directions=entry[4],
        description=entry[5],
        up_votes=entry[6],
        down_votes=entry[7],
    )

    return new_report


@app.get("/api/v0/reports/")
async def get_all_posts():
    db_cursor.execute("SELECT * FROM reports WHERE deleted_at IS NULL;")
    rows = db_cursor.fetchall()

    return rows_to_reports(rows)


@app.get("/api/v0/reports/{report_id}")
async def get_one_post(report_id):
    sql = "SELECT * FROM reports WHERE id = %s AND deleted_at IS NULL;"
    db_cursor.execute(sql, (report_id,))
    row = db_cursor.fetchone()

    if row is None:
        return {"message": "report does not exist"}

    report = Report(
        id=row[0],
        timestamp=row[1],
        title=row[2],
        location=row[3],
        directions=row[4],
        description=row[5],
        up_votes=row[6],
        down_votes=row[7],
    )

    return report


@app.put("/api/v0/reports/delete/{report_id}")
async def delete_report(report_id):
    sql1 = (
        "UPDATE reports SET deleted_at = %s WHERE id = %s AND deleted_at "
        "IS NULL RETURNING title, deleted_at;"
    )
    utc_now = datetime.datetime.now(datetime.UTC)
    db_cursor.execute(sql1, (utc_now, report_id))
    row = db_cursor.fetchone()
    db_connection.commit()

    if row is None:
        return {"message": "report not deleted"}

    return {"message": "report deleted", "title": row[0], "deleted_at": row[1]}
