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

**FastAPI API Gateway**  
Handles incoming requests and orchestrates the AI pipeline.

**Language Detection**  
Identifies whether the conversation is in English, Hindi, or Tamil.

**Agent Reasoning Layer**  
Local LLM inference using Phi3 via Ollama to interpret patient intent and decide which backend tool to call.

**Hybrid Intent Routing**  
To maintain low latency, the system includes a fast rule-based router that handles common scheduling intents instantly.  
More complex conversational requests fall back to LLM reasoning.

**Tool Orchestration**  
Routes AI decisions to backend tools such as appointment scheduling.

**Appointment Scheduler**  
Handles booking, cancellation, rescheduling, and conflict detection.

**Memory Layer (Redis)**  
Stores patient session context and appointment history.

**Campaign Engine**  
Triggers outbound appointment reminder campaigns.

---

## Multilingual Support

The system supports three Indian languages:

English  
Hindi  
Tamil  

Language detection is performed automatically using a lightweight detection module.

Language preference can be associated with a patient ID and stored in Redis memory so returning patients continue conversations in their preferred language.

---

## Latency Design

Target latency defined in the assignment:

**<450 ms from speech end to first response**

Pipeline latency breakdown:

Input Processing  
→ Language Detection  
→ Agent Reasoning  
→ Tool Execution  
→ Response Generation

### Performance Optimization Strategy

The system uses a **hybrid reasoning architecture**:

Fast rule-based intent routing  
→ Handles common booking requests instantly.

LLM reasoning fallback  
→ Used only when complex natural language understanding is required.

This design significantly reduces latency compared to sending every request through the LLM.

### Prototype Latency Note

In this prototype the LLM runs locally on CPU via Ollama, which increases inference latency.

In a production environment this would be optimized using:

GPU inference  
model quantization  
high-performance model serving

---

## Memory Design

The system maintains two levels of context.

### Session Memory

Stored temporarily in Redis using TTL.

Example:

```
session:patient_1
{
  doctor: "Dr Mehta",
  time: "4pm"
}
```

This allows the system to track the current conversation state.

### Historical Memory

Redis can also maintain historical interactions such as:

preferred doctors  
past appointments  
language preference

This enables context-aware responses like:

"Book with my usual doctor."

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

The agent can proactively contact patients for reminder campaigns.

Example flow:

Campaign Engine  
→ Fetch upcoming appointments  
→ Send reminder message  
→ AI processes patient response  
→ Confirm / Cancel / Reschedule appointment

This simulates automated healthcare reminder calls.

---

## Tradeoffs

### Local LLM vs Cloud API

Local inference was chosen to:

reduce external dependencies  
improve patient data privacy  
avoid API usage costs

Tradeoff:

CPU inference introduces higher latency compared to GPU-based systems.

---

### Redis vs Traditional Database

Redis was selected because it provides:

fast key-value retrieval  
session TTL support  
low-latency memory storage

Tradeoff:

Redis is not ideal for long-term persistent healthcare records.

---

## Scalability Design

The architecture is designed to scale horizontally.

Stateless FastAPI servers allow multiple instances to run behind a load balancer.

Redis acts as a shared memory layer across all agent instances.

This allows the system to scale for large numbers of concurrent patient conversations.

Future architecture could include:

background job queues for campaign scheduling  
distributed model inference services  
containerized microservices deployment

---

## Future Improvements

Real-time streaming speech pipeline  
GPU optimized inference  
Twilio telephony integration  
Doctor availability database  
Distributed campaign scheduling

Target latency: **<450ms from speech end to first audio response.**

---

## Running the Project

Install dependencies

```
pip install -r requirements.txt
```

Start Ollama

```
ollama serve
```

Run the backend

```
uvicorn backend.main:app --reload
```

Open API docs

```
http://127.0.0.1:8000/docs
```

---

## Demo Endpoints

POST `/voice`  
Handles patient interaction with the AI agent.

GET `/campaign/reminders`  
Triggers outbound reminder campaign.

GET `/health`  
System health monitoring endpoint.

---

## Author

Aditya Khamait