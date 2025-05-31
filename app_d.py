
import streamlit as st
from fpdf import FPDF
import os

# Custom PDF class with two-column layout and Unicode support
class MyPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
        self.set_font("DejaVu", "", 9)

    def add_patient_block(self, text, col, row_height):
        col_width = 95
        x_margin = 10 + (col * (col_width + 5))
        y_pos = self.get_y()
        self.set_xy(x_margin, y_pos)
        self.multi_cell(col_width, row_height, text, border=1)

st.set_page_config(page_title="Structured Handoff (Two Column)", layout="centered")
st.title("📋 Surgical Handoff Entry (Two Column PDF)")

if "patients" not in st.session_state:
    st.session_state.patients = []

def format_patient(index, data):
    def add(label, value):
        return f"{label}: {value}" if value.strip() else ""

    def add_list(label, values):
        lines = [f"{label}:"]
        lines += [f"{i+1}. {val}" for i, val in enumerate(values) if val.strip()]
        return "\n".join(lines) if len(lines) > 1 else ""

    fields = [
        f"Patient #{index + 1}",
        "Patient Medical Record",
        add("Name", data["name"]),
        add("Room", data["room"]),
        add("Specialist", data["specialist"]),
        add("Age", data["age"]),
        add("Allergy", data["allergy"]),
        add("PM Hx", data["pmhx"]),
        add("PS Hx", data["pshx"]),
        add("Diagnosis", data["diagnosis"]),
        add("Operation", data["operation"]),
        add("Diet", data["diet"]),
        add("IVF", data["ivf"]),
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
        add("- NGT", data["ngt"]),
        add("- Drain", data["drain"]),
        add("- Chest Tube", data["chest_tube"]),
        add("- Stoma", data["stoma"]),
        add_list("Medications", data["meds"]),
        add("DVT Prophylaxis", data["dvt"]),
        add("Analgesia", data["analgesia"]),
        "Important Notes:",
        data["notes"] if data["notes"].strip() else "",
        add("Consultation", data["consult"]),
    ]
    return "\n".join([f for f in fields if f.strip()])

def generate_dual_pdf(patients):
    pdf = MyPDF()
    pdf.add_page()
    row_height = 5
    col = 0

    for i, patient in enumerate(patients):
        text = format_patient(i, patient)
        pdf.add_patient_block(text, col, row_height)
        col = (col + 1) % 2
        if col == 0:
            pdf.ln(65)  # Space between rows

    pdf.output("handoff_dual_column.pdf")

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
    foley = st.text_input("Foley")
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
        st.session_state.patients.append({
            "name": name, "room": room, "specialist": specialist,
            "age": age, "allergy": allergy, "pmhx": pmhx, "pshx": pshx,
            "diagnosis": diagnosis, "operation": operation, "diet": diet,
            "ivf": ivf, "bp": bp, "hr": hr, "rr": rr, "temp": temp,
            "amb": amb, "uri": uri, "eat": eat, "dress": dress,
            "foley": foley, "ngt": ngt, "drain": drain,
            "chest_tube": chest_tube, "stoma": stoma, "meds": meds,
            "dvt": dvt, "analgesia": analgesia, "notes": notes, "consult": consult
        })
        st.success("Patient added.")

if st.session_state.patients:
    st.subheader("📄 Final Report")
    if st.button("📥 Download Two-Column PDF"):
        generate_dual_pdf(st.session_state.patients)
        with open("handoff_dual_column.pdf", "rb") as f:
            st.download_button("⬇️ Download PDF", f, file_name="handoff_dual_column.pdf", mime="application/pdf")
