
import streamlit as st
from datetime import datetime
from fpdf import FPDF

class MyPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
        self.set_font('DejaVu', '', 11)

def generate_pdf(text, filename="handoff_report.pdf"):
    pdf = MyPDF()
    pdf.add_page()
    for line in text.split("\n"):
        pdf.multi_cell(0, 8, line)
    pdf.output(filename)

st.set_page_config(page_title="Structured Handoff Form", layout="centered")
st.title("📋 Surgical Handoff Entry")

if "patients" not in st.session_state:
    st.session_state.patients = []

def format_patient(data):
    def add(label, value):
        return f"{label}: {value}" if value.strip() else ""

    def add_list(label, values):
        items = [v for v in values if v.strip()]
        if items:
            lines = [f"{label}:"]
            for i, val in enumerate(items, 1):
                lines.append(f"{i}. {val}")
            return "\n".join(lines)
        return ""

    block = [
        "Patient Medical Record",
        add("Name", data["name"]),
        add("Room", data["room"]),
        add("Specialist", data["specialist"]),
        add("Age", data["age"]),
        add("Allergy", data["allergy"]),
        add("PM Hx (Past Medical History)", data["pmhx"]),
        add("PS Hx (Past Surgical History)", data["pshx"]),
        add("Diagnosis", data["diagnosis"]),
        add("Operation", data["operation"]),
        add("Diet", data["diet"]),
        add("IVF (Intravenous Fluids)", data["ivf"]),
        "Vital Signs (V/S):",
        f"BP: {data['bp']}" if data["bp"].strip() else "",
        f"HR: {data['hr']}" if data["hr"].strip() else "",
        f"RR: {data['rr']}" if data["rr"].strip() else "",
        f"Temp: {data['temp']}" if data["temp"].strip() else "",
        "✓ Ambulation" if data["amb"] else "",
        "✓ Urination" if data["uri"] else "",
        "✓ Diet" if data["eat"] else "",
        "✓ Dress" if data["dress"] else "",
        "Medical Devices:",
        add("- Foley's", data["foley"]),
        add("- NGT (NasoGastric Tube)", data["ngt"]),
        add("- Drain", data["drain"]),
        add("- Chest Tube", data["chest_tube"]),
        add("- Stoma", data["stoma"]),
        add_list("Medications", data["meds"]),
        add("DVT Prophylaxis", data["dvt"]),
        add("Analgesia", data["analgesia"]),
        "Important Notes:",
        data["notes"] if data["notes"].strip() else "",
        add("Consultation", data["consult"]),
        "-"*60
    ]
    return "\n".join([line for line in block if line.strip()])

with st.form("form", clear_on_submit=True):
    name = st.text_input("Name")
    room = st.text_input("Room")
    specialist = st.text_input("Specialist")
    age = st.text_input("Age")
    allergy = st.text_input("Allergy")
    pmhx = st.text_area("Past Medical History")
    pshx = st.text_area("Past Surgical History")
    diagnosis = st.text_area("Diagnosis")
    operation = st.text_area("Operation")
    diet = st.text_input("Diet")
    ivf = st.text_input("IV Fluids")
    bp = st.text_input("BP")
    hr = st.text_input("HR")
    rr = st.text_input("RR")
    temp = st.text_input("Temp")
    amb = st.checkbox("Ambulation")
    uri = st.checkbox("Urination")
    eat = st.checkbox("Diet Tolerance")
    dress = st.checkbox("Dressing Change")
    foley = st.text_input("Foley's")
    ngt = st.text_input("NGT")
    drain = st.text_input("Drain")
    chest_tube = st.text_input("Chest Tube")
    stoma = st.text_input("Stoma")
    meds = [st.text_input(f"Medication {i+1}") for i in range(7)]
    dvt = st.text_input("DVT Prophylaxis")
    analgesia = st.text_input("Analgesia")
    notes = st.text_area("Important Notes")
    consult = st.text_input("Consultation")

    submit = st.form_submit_button("➕ Add Patient")
    if submit:
        patient = {
            "name": name, "room": room, "specialist": specialist,
            "age": age, "allergy": allergy, "pmhx": pmhx, "pshx": pshx,
            "diagnosis": diagnosis, "operation": operation, "diet": diet,
            "ivf": ivf, "bp": bp, "hr": hr, "rr": rr, "temp": temp,
            "amb": amb, "uri": uri, "eat": eat, "dress": dress,
            "foley": foley, "ngt": ngt, "drain": drain, "chest_tube": chest_tube,
            "stoma": stoma, "meds": meds, "dvt": dvt, "analgesia": analgesia,
            "notes": notes, "consult": consult
        }
        st.session_state.patients.append(patient)
        st.success("Patient added.")

if st.session_state.patients:
    st.subheader("📄 Final Report")
    full_text = "\n\n".join([format_patient(p) for p in st.session_state.patients])
    st.text_area("Patient Report", full_text, height=600)

    if st.button("📥 Download as PDF"):
        generate_pdf(full_text)
        with open("handoff_report.pdf", "rb") as f:
            st.download_button("⬇️ Click here to download PDF", f, file_name="handoff_report.pdf", mime="application/pdf")
