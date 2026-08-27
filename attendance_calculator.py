import sqlite3


DATABASE_NAME = "attendance.db"


def get_attendance(
    student_id,
    subject
):

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            COUNT(*),
            SUM(
                CASE
                    WHEN status = 'Present'
                    THEN 1
                    ELSE 0
                END
            )
        FROM attendance
        WHERE student_id = ?
        AND subject = ?
        """,
        (
            student_id,
            subject
        )
    )

    result = cursor.fetchone()

    conn.close()

    total = result[0] or 0

    present = result[1] or 0

    absent = total - present

    if total > 0:

        percentage = (
            present / total
        ) * 100

    else:

        percentage = 0

    return {

        "total": total,

        "present": present,

        "absent": absent,

        "percentage": percentage

    }


def get_recent_attendance(
    student_id,
    subject,
    limit=5
):

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT status
        FROM attendance
        WHERE student_id = ?
        AND subject = ?
        ORDER BY date DESC
        LIMIT ?
        """,
        (
            student_id,
            subject,
            limit
        )
    )

    records = cursor.fetchall()

    conn.close()

    if not records:

        return 0

    present = sum(

        1

        for record in records

        if record[0] == "Present"

    )

    percentage = (
        present / len(records)
    ) * 100

    return percentage