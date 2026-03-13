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