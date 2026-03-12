appointments = []

def book_appointment(patient_id, doctor, time):

    for appt in appointments:
        if appt["doctor"] == doctor and appt["time"] == time:
            return {
                "status": "conflict",
                "message": "This slot is already booked. Please choose another time."
            }

    appointment = {
        "patient_id": patient_id,
        "doctor": doctor,
        "time": time
    }

    appointments.append(appointment)

    return {
        "status": "confirmed",
        "message": f"Appointment booked with {doctor} at {time}"
    }


def cancel_appointment(patient_id):

    for appt in appointments:
        if appt["patient_id"] == patient_id:
            appointments.remove(appt)
            return {"status": "cancelled"}

    return {"status": "not_found"}


def reschedule_appointment(patient_id, new_time):

    for appt in appointments:
        if appt["patient_id"] == patient_id:
            appt["time"] = new_time
            return {"status": "rescheduled"}

    return {"status": "not_found"}