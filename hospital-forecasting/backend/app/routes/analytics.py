import pandas as pd
from flask import Blueprint, jsonify
from app.utils.admissions_loader import load_latest_admissions_data

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/department", methods=["GET"])
def admissions_by_department():
    df = load_latest_admissions_data()
    df["admit_date"] = pd.to_datetime(df["admit_date"])
    df["day"] = df["admit_date"].dt.strftime("%Y-%m-%d")

    grouped = df.groupby(["day", "dept"]).size().unstack(fill_value=0).sort_index()
    labels = grouped.index.tolist()
    datasets = [
        {
            "label": dept,
            "data": grouped[dept].tolist()
        }
        for dept in grouped.columns
    ]
    return jsonify({"labels": labels, "datasets": datasets})
