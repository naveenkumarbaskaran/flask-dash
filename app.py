from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///analytics.db"
db = SQLAlchemy(app)


class PageView(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(256), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_agent = db.Column(db.String(512))
    ip_address = db.Column(db.String(45))


@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/track", methods=["POST"])
def track():
    from flask import request
    view = PageView(
        path=request.json.get("path", "/"),
        user_agent=request.headers.get("User-Agent"),
        ip_address=request.remote_addr,
    )
    db.session.add(view)
    db.session.commit()
    return jsonify({"status": "ok"})


@app.route("/api/stats")
def stats():
    from sqlalchemy import func
    daily = (
        db.session.query(
            func.date(PageView.timestamp).label("date"),
            func.count(PageView.id).label("count"),
        )
        .group_by(func.date(PageView.timestamp))
        .order_by(func.date(PageView.timestamp))
        .limit(30)
        .all()
    )
    return jsonify([{"date": str(d), "count": c} for d, c in daily])


if __name__ == "__main__":
    app.run(debug=True)
