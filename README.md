# ArogyaVoice

Real-Time Multilingual Voice AI Agent for Clinical Appointment Booking.

---

## Overview

ArogyaVoice is a conversational AI system designed to handle clinical appointment management through natural voice interactions.

The agent supports multilingual conversations (English, Hindi, Tamil), maintains contextual memory across sessions, and can initiate outbound reminder campaigns.

The system demonstrates real-time AI reasoning, tool orchestration, memory management, and scheduling logic.

---

## System Architecture

```
Patient Voice / Text
        │
        ▼
FastAPI API Gateway (/voice)
        │
        ▼
Language Detection
        │
        ▼
Agent Reasoning Layer (Ollama + Phi3)
        │
        ├── Tool: Appointment Scheduler
        │       ├─ Conflict Detection
        │       └─ Slot Allocation
        │
        ├── Memory Layer (Redis)
        │       ├─ Session Context
        │       └─ Patient History
        │
        └── Campaign Engine
                └─ Appointment Reminder Calls

        ▼
Response Generator
        │
        ▼
Voice / Text Output
```

---

## Core Components

FastAPI API Gateway  
Handles incoming requests and orchestrates the AI pipeline.

Language Detection  
Identifies whether the conversation is in English, Hindi, or Tamil.

Agent Reasoning Layer  
Local LLM inference using Phi3 via Ollama to interpret patient intent.

Tool Orchestration  
Routes AI decisions to backend tools such as appointment scheduling.

Appointment Scheduler  
Handles booking, cancellation, rescheduling, and conflict detection.

Memory Layer (Redis)  
Stores patient session context and appointment history.

Campaign Engine  
Triggers outbound appointment reminder campaigns.

---

## Latency Design

Target latency defined in the assignment:  
<450 ms from speech end to first response.

Pipeline latency breakdown:

Input Processing
→ Language Detection
→ LLM Reasoning
→ Tool Execution
→ Response Generation

Latency optimization strategies:

Local LLM inference (Ollama)
Redis in-memory session storage
Lightweight scheduling logic
FastAPI async request handling

---

## Memory Design

The system maintains two levels of context:

Session Memory  
Stored temporarily in Redis using TTL.

Example:

session:patient_1
{
  doctor: "Dr Mehta",
  time: "4pm"
}

Historical Memory  
Tracks previous appointments and patient preferences.

This allows the agent to understand requests like:

"Book with my usual doctor"

---

## Appointment Scheduling Logic

The scheduling engine prevents invalid bookings.

Handled scenarios:

Doctor slot conflicts
Past time selection
Unavailable doctors
Rescheduling existing appointments

Example:

User Request
Book appointment with Dr Mehta at 4pm

If slot already booked
→ Conflict detected
→ Alternative time suggested

---

## Outbound Campaign Mode

The agent can proactively contact patients for reminders.

Example flow:

Campaign Engine
→ Fetch upcoming appointments
→ Send reminder message
→ AI processes patient response
→ Confirm / Cancel / Reschedule appointment

This simulates automated healthcare reminder calls.

---

## Tradeoffs

Local LLM vs Cloud API

Local inference was chosen to:

reduce external dependencies  
improve data privacy  
avoid API costs  

Tradeoff:  
CPU inference introduces slightly higher latency.

Redis vs Traditional Database

Redis was selected because it provides:

fast key-value access  
session TTL support  
low-latency memory storage  

Tradeoff:  
not suited for long-term persistent storage.

---

## Future Improvements

Real-time streaming speech pipeline  
GPU optimized inference  
Twilio telephony integration  
Doctor availability database  
Distributed campaign scheduling

Target latency: <450ms from speech end to first audio response.
---

## Running the Project

Install dependencies

pip install -r requirements.txt

Start Ollama

ollama serve

Run the backend

uvicorn backend.main:app --reload

Open API docs

http://127.0.0.1:8000/docs

---

## Demo Endpoints

POST /voice  
Handles patient interaction with the AI agent.

GET /campaign/reminders  
Triggers outbound reminder campaign.

---

## Author

Aditya Khamait