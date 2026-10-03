from flask import Flask, render_template_string
from dotenv import load_dotenv
import boto3
import os
import pymysql

load_dotenv()

app = Flask(__name__)

# HTML template for displaying Borromean Digital Events
PAGE = """
<!doctype html>
<html>
<head>
    <title>Borromean Digital Events</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1000px;
            margin: 40px auto;
            padding: 0 20px;
        }

        h1 {
            color: #00274C;
        }

        .event {
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 20px;
            display: flex;
            gap: 20px;
            align-items: center;
        }

        .event img {
            width: 180px;
            height: 120px;
            object-fit: cover;
            border-radius: 6px;
        }

        .event-info {
            flex: 1;
        }

        .event-name {
            font-size: 1.3rem;
            font-weight: bold;
            color: #00274C;
            margin-bottom: 8px;
        }

        .event-detail {
            margin: 4px 0;
        }
    </style>
</head>

<body>
    <h1>Borromean Digital Events</h1>
    <p>Upcoming company events from RDS, with event images stored in S3.</p>

    {% for event in events %}
    <div class="event">
        <img src="{{ event.image_url }}" alt="{{ event.name }}">

        <div class="event-info">
            <div class="event-name">{{ event.name }}</div>
            <div class="event-detail"><strong>Date:</strong> {{ event.event_date }}</div>
            <div class="event-detail"><strong>Location:</strong> {{ event.location }}</div>
        </div>
    </div>
    {% endfor %}
</body>
</html>
"""


def get_database_rows():
    conn = pymysql.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASS"],
        database=os.environ["DB_NAME"],
        connect_timeout=5,
    )

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT name, event_date, location, image_key
                FROM events
                ORDER BY event_date
                """
            )
            return cur.fetchall()
    finally:
        conn.close()


def get_events():
    bucket_name = os.environ["S3_BUCKET"]
    s3 = boto3.client("s3")

    rows = get_database_rows()
    events = []

    for name, event_date, location, image_key in rows:
        # Verify that the object exists in S3.
        # This also makes a bad S3 configuration visible to students.
        s3.head_object(
            Bucket=bucket_name,
            Key=image_key,
        )

        # Generate a temporary URL so the bucket can remain private.
        image_url = s3.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": bucket_name,
                "Key": image_key,
            },
            ExpiresIn=3600,
        )

        events.append(
            {
                "name": name,
                "event_date": event_date,
                "location": location,
                "image_key": image_key,
                "image_url": image_url,
            }
        )

    return events


@app.route("/")
def home():
    try:
        return render_template_string(
            PAGE,
            events=get_events(),
        )
    except Exception as err:
        return (
            f"""
            <h1>Something broke</h1>
            <p>The application encountered an error while loading event data.</p>
            <pre>{err}</pre>
            """,
            500,
        )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
    )
