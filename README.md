# 🧮 FastAPI Parallel Fibonacci Backend

A simple backend built with **FastAPI** that performs **parallel Fibonacci computations** using Python’s multiprocessing and threading capabilities.

---

## 🚀 Features
- Submit jobs for heavy computations in parallel
- Check job status and retrieve results
- Supports both synchronous and asynchronous computation
- Built with **FastAPI** + **Uvicorn**
- Ready for deployment on Vercel

---

## 🧱 Project Structure

fibonacci-project/
│
├── fastapi_parallel_backend.py # Main FastAPI backend file
├── requirements.txt # Python dependencies
├── frontend/ # Frontend HTML + JS (optional)
└── README.md # Project documentation

---


🧠 API Endpoints
Endpoint	Method	Description
/submit	POST	Submit a list of numbers for Fibonacci computation
/status/{job_id}	GET	Check the status of a job
/result/{job_id}	GET	Retrieve the result once finished
/compute-sync	POST	Run synchronous computation immediately
/compute-async	POST	Run asynchronous computation
/health	GET	Health check endpoint

---

Backend file:  
fastapi_parallel_backend.py

yaml
Copy code

Main endpoints:
| URL | Method | Description |
|------|--------|-------------|
| `/submit` | POST | Submit a list of numbers for parallel computation |
| `/status/{job_id}` | GET | Check the status of a submitted job |
| `/result/{job_id}` | GET | Get the result of a finished job |
| `/compute-sync` | POST | Perform synchronous (immediate) calculation |
| `/compute-async` | POST | Perform async computation using process pool |
| `/health` | GET | Check server health |

---

### 💻 Frontend — HTML + JavaScript
The frontend is a simple, user-friendly webpage that:
- Lets you enter a list of numbers  
- Sends the data to the backend via **fetch()**
- Displays real-time job status and final results

Frontend file:  
rontend/index.html


To run the frontend locally:
```bash
cd frontend
python -m http.server 5500
