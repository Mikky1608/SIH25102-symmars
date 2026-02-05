import os
import smtplib
import ssl
import pandas as pd
from email.message import EmailMessage
from dataclasses import dataclass
from typing import Optional

# --- Config from environment (set these for the demo) ---
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")

# Twilio-style SMS (optional demo)
TWILIO_SID = os.getenv("TWILIO_SID", "")
TWILIO_AUTH = os.getenv("TWILIO_AUTH", "")
TWILIO_FROM = os.getenv("TWILIO_FROM", "")

# MSG91 or generic SMS provider (optional demo)
SMS_API_KEY = os.getenv("SMS_API_KEY", "")

# --- Dataclasses ---
@dataclass
class Contact:
    name: str
    email: Optional[str]
    phone: Optional[str]

# --- Email / SMS helpers ---
def send_email(to_email: str, subject: str, body: str, sender_name: str = "Counseling Desk"):
    if not to_email:
        return False, "missing email"
    msg = EmailMessage()
    msg["From"] = f"{sender_name} <{SMTP_USER}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        return True, "sent"
    except Exception as e:
        return False, str(e)

def send_sms_twilio(to_phone: str, body: str):
    if not (TWILIO_SID and TWILIO_AUTH and TWILIO_FROM and to_phone):
        return False, "twilio not configured"
    try:
        # Lazy import to keep prototype minimal
        from twilio.rest import Client
        client = Client(TWILIO_SID, TWILIO_AUTH)
        message = client.messages.create(body=body, from_=TWILIO_FROM, to=to_phone)
        return True, message.sid
    except Exception as e:
        return False, str(e)

# Stub for generic SMS vendor; implement requests.post if needed
def send_sms_stub(to_phone: str, body: str):
    if not (SMS_API_KEY and to_phone):
        return False, "sms vendor not configured"
    # For prototype: print to console to simulate
    print(f"[SMS-> {to_phone}] {body[:120]}...")
    return True, "stubbed"

# --- Loading contacts ---
def load_mentors(mentor_files):
    dfs = []
    for path in mentor_files:
        df = pd.read_csv(path)
        # Expected columns: mentor_id, mentor_name, mentor_email?, mentor_phone?
        # If column headers differ slightly, adjust here but DO NOT modify file contents:
        # e.g., 'mentorid' -> 'mentor_id'
        cols = {c.lower(): c for c in df.columns}
        def pick(name_variants, row):
            for v in name_variants:
                if v in cols:
                    return row[cols[v]]
            return None
        out = []
        for _, row in df.iterrows():
            mid = pick(["mentor_id","mentorid"], row)
            mname = pick(["mentor_name","mentorname"], row)
            memail = pick(["mentor_email","email"], row)
            mphone = pick(["mentor_phone","phone"], row)
            out.append({"mentor_id": mid, "mentor_name": mname, "mentor_email": memail, "mentor_phone": mphone})
        dfs.append(pd.DataFrame(out))
    return pd.concat(dfs, ignore_index=True).drop_duplicates(subset=["mentor_id"])

def load_parents(parent_files):
    dfs = []
    for path in parent_files:
        df = pd.read_csv(path)
        cols = {c.lower(): c for c in df.columns}
        def pick(name_variants, row):
            for v in name_variants:
                if v in cols:
                    return row[cols[v]]
            return None
        out = []
        for _, row in df.iterrows():
            pid = pick(["parent_id","parentid"], row)
            pname = pick(["parent_name","parentname"], row)
            pemail = pick(["parent_email","email"], row)
            pphone = pick(["parent_phone","phone"], row)
            out.append({"parent_id": pid, "parent_name": pname, "parent_email": pemail, "parent_phone": pphone})
        dfs.append(pd.DataFrame(out))
    return pd.concat(dfs, ignore_index=True).drop_duplicates(subset=["parent_id"])

# --- Main senders ---
def send_to_mentors(alerts_csv, mentor_files, channel="email"):
    mentors = load_mentors(mentor_files)
    alerts = pd.read_csv(alerts_csv)
    # alerts must have: mentor_id, message_mentor
    sent, failed = [], []
    for _, row in alerts.iterrows():
        mid = row.get("mentor_id") or row.get("mentorid")
        msg = row.get("message_mentor")
        if pd.isna(mid) or pd.isna(msg):
            failed.append(("missing_fields", None))
            continue
        m = mentors[mentors["mentor_id"] == mid]
        if m.empty:
            failed.append(("mentor_not_found", int(mid)))
            continue
        memail = m.iloc[0].get("mentor_email")
        mphone = m.iloc[0].get("mentor_phone")
        ok = False
        info = ""
        if channel == "email":
            ok, info = send_email(memail, subject="At-risk students: weekly digest", body=msg)
        elif channel == "twilio":
            ok, info = send_sms_twilio(mphone, body=msg)
        elif channel == "sms_stub":
            ok, info = send_sms_stub(mphone, body=msg)
        else:
            failed.append(("unknown_channel", channel))
            continue
        (sent if ok else failed).append((int(mid), info))
    return sent, failed

def send_to_parents(alerts_csv, parent_files, channel="email"):
    parents = load_parents(parent_files)
    alerts = pd.read_csv(alerts_csv)
    # alerts must have: parent_id, message_parent
    sent, failed = [], []
    for _, row in alerts.iterrows():
        pid = row.get("parent_id") or row.get("parentid")
        msg = row.get("message_parent")
        if pd.isna(pid) or pd.isna(msg):
            failed.append(("missing_fields", None))
            continue
        p = parents[parents["parent_id"] == pid]
        if p.empty:
            failed.append(("parent_not_found", int(pid)))
            continue
        pemail = p.iloc[0].get("parent_email")
        pphone = p.iloc[0].get("parent_phone")
        ok = False
        info = ""
        if channel == "email":
            ok, info = send_email(pemail, subject="Attendance support update", body=msg)
        elif channel == "twilio":
            ok, info = send_sms_twilio(pphone, body=msg)
        elif channel == "sms_stub":
            ok, info = send_sms_stub(pphone, body=msg)
        else:
            failed.append(("unknown_channel", channel))
            continue
        (sent if ok else failed).append((int(pid), info))
    return sent, failed

if __name__ == "__main__":
    # Example usage (adjust paths):
    # alerts.csv contains columns: mentor_id, parent_id, message_mentor, message_parent
    ALERTS = "alerts.csv"

    mentor_files = ["Mentors_Institute1.csv", "Mentors_Institute2.csv"]
    parent_files = ["Parents_Institute1.csv", "Parents_Institute2.csv"]

    print("Sending mentor notifications (email)...")
    m_ok, m_fail = send_to_mentors(ALERTS, mentor_files, channel="email")
    print("Mentor sent:", m_ok)
    print("Mentor failed:", m_fail)

    print("Sending parent notifications (email)...")
    p_ok, p_fail = send_to_parents(ALERTS, parent_files, channel="email")
    print("Parent sent:", p_ok)
    print("Parent failed:", p_fail)
