import pandas as pd
from flask import Blueprint, jsonify
from app.utils.admissions_loader import load_latest_admissions_data
from app.utils.procedures_loader import load_latest_procedures_data
from app.utils.staffing_loader import load_latest_staffing_data
from app.utils.beds_loader import load_latest_beds_data

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/department", methods=["GET"])
def admissions_by_department():
    df = load_latest_admissions_data()
    df["admit_date"] = pd.to_datetime(df["admit_date"])
    df["day"] = df["admit_date"].dt.strftime("%Y-%m-%d")

    grouped = df.groupby(["day", "dept"]).size().unstack(fill_value=0).sort_index()
    labels = grouped.index.tolist()
    datasets = [
        {"label": dept, "data": grouped[dept].tolist()}
        for dept in grouped.columns
    ]
    return jsonify({"labels": labels, "datasets": datasets})


@analytics_bp.route("/procedures", methods=["GET"])
def procedures_by_type():
    df = load_latest_procedures_data()
    df["date"] = pd.to_datetime(df["date"])
    df["day"] = df["date"].dt.strftime("%Y-%m-%d")

    grouped = df.groupby(["day", "procedure"]).size().unstack(fill_value=0).sort_index()
    labels = grouped.index.tolist()
    datasets = [
        {"label": proc, "data": grouped[proc].tolist()}
        for proc in grouped.columns
    ]
    return jsonify({"labels": labels, "datasets": datasets})


@analytics_bp.route("/staffing", methods=["GET"])
def staff_hours_by_dept():
    df = load_latest_staffing_data()
    grouped = df.groupby(["shift_date", "department"])["hours"].sum().unstack(fill_value=0).sort_index()
    labels = grouped.index.tolist()
    datasets = [
        {"label": dept, "data": grouped[dept].tolist()}
        for dept in grouped.columns
    ]
    return jsonify({"labels": labels, "datasets": datasets})


@analytics_bp.route("/beds", methods=["GET"])
def icu_vs_beds_occupancy():
    df = load_latest_beds_data()
    df["start_time"] = pd.to_datetime(df["start_time"])
    df["day"] = df["start_time"].dt.strftime("%Y-%m-%d")

    grouped = df.groupby(["day", "is_ICU"]).size().unstack(fill_value=0).sort_index()
    grouped.columns = ["Non-ICU", "ICU"] if 0 in grouped.columns and 1 in grouped.columns else grouped.columns
    labels = grouped.index.tolist()
    datasets = [
        {"label": str(col), "data": grouped[col].tolist()}
        for col in grouped.columns
    ]
    return jsonify({"labels": labels, "datasets": datasets})
