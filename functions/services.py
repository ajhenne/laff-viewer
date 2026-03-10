import streamlit as st
import requests


def record_pageview():

    query_ref = st.query_params.get("ref", None)

    headers = st.context.headers
    user_agent = headers.get("User-Agent", "Streamlit-App")

    ip = headers.get("X-Forwarded-For", "0.0.0.0").split(",")[0]
    if not ip or ip == "0.0.0.0":
        ip = st.context.ip_address

    url = "https://ajhenne.goatcounter.com/api/v0/count"
    token = st.secrets["goatcounter_key"]

    page_path = st.context.url.replace(st.context.headers.get("Host", ""), "").split(
        "?"
    )[0]

    payload = {
        "no_sessions": False,
        "hits": [
            {
                "path": page_path,
                "title": page_path.strip("/").replace("-", " ").title(),
                "event": False,
                "ip": ip,
                "user_agent": user_agent,
                "referrer": query_ref or headers.get("Referer", ""),
            }
        ],
    }

    try:
        requests.post(
            url, json=payload, headers={"Authorization": f"Bearer {token}"}, timeout=1
        )
    except Exception:
        pass
