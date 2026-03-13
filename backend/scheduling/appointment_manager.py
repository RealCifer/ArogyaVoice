import json
from backend.utils.logger import logger

# Load doctor data
with open("data/doctors.json", "r") as f:
    DOCTORS = json.load(f)

# In-memory appointment store
appointments = []


def find_doctor(doctor_name):
    """
    Find doctor by name
    """
    return next((d for d in DOCTORS if d["name"].lower() == doctor_name.lower()), None)


def book_appointment(patient_id: str, doctor: str, time: str):

    logger.info(f"Booking request: patient={patient_id}, doctor={doctor}, time={time}")

    doctor_data = find_doctor(doctor)

    if not doctor_data:
        logger.error("Doctor not found")
        return {"error": "doctor_not_found", "available_doctors": [d["name"] for d in DOCTORS]}

    if time not in doctor_data["available_slots"]:
        logger.warning("Requested slot unavailable")
        return {
            "error": "slot_unavailable",
            "available_slots": doctor_data["available_slots"]
        }

    for appt in appointments:
        if appt["doctor"] == doctor and appt["time"] == time:
            logger.warning("Slot already booked")
            return {"error": "slot_already_booked"}

    appointment = {
        "patient_id": patient_id,
        "doctor": doctor,
        "time": time
    }

    appointments.append(appointment)

    logger.info(f"Appointment confirmed: {appointment}")

    return {
        "status": "confirmed",
        "appointment": appointment
    }


def cancel_appointment(patient_id: str):

    for appt in appointments:
        if appt["patient_id"] == patient_id:
            appointments.remove(appt)
            logger.info(f"Appointment cancelled for patient {patient_id}")
            return {"status": "cancelled"}

    return {"error": "appointment_not_found"}


def reschedule_appointment(patient_id: str, new_time: str):

    for appt in appointments:
        if appt["patient_id"] == patient_id:
            appt["time"] = new_time
            logger.info(f"Appointment rescheduled: {appt}")
            return {"status": "rescheduled", "appointment": appt}

    return {"error": "appointment_not_found"}