appointments = []

available_doctors = [
    "Dr Sharma",
    "Dr Mehta",
    "Dr Rao",
    "Dr Patel"
]


def book_appointment(patient_id, doctor, time):

    if doctor not in available_doctors:
        return {
            "status": "doctor_not_available",
            "available_doctors": available_doctors
        }

    for appt in appointments:
        if appt["doctor"] == doctor and appt["time"] == time:
            return {
                "status": "conflict",
                "message": f"{doctor} already has an appointment at {time}"
            }

    appointment = {
        "patient_id": patient_id,
        "doctor": doctor,
        "time": time
    }

    appointments.append(appointment)

    return {
        "status": "confirmed",
        "doctor": doctor,
        "time": time
    }