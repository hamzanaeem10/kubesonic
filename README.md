# Kube-Sonic: Event-Driven Autoscaling AI Cluster 🚀

A production-grade, event-driven microservices architecture for serving AI inference models. Designed to handle bursty workloads by dynamically scaling worker pods from **0 to N** based on real-time queue depth.

## 📊 Live Autoscaling Demo
**"The Pulse of the Cluster"**
Below is a real-time Grafana dashboard capturing a traffic burst.
* **Yellow Line (Cause):** Network traffic hits Redis (Job Queue fills up).
* **Green Steps (Effect):** KEDA triggers the Horizontal Pod Autoscaler, provisioning new worker pods in steps to handle the load.

<img width="1838" height="842" alt="image" src="https://github.com/user-attachments/assets/93baf1ea-ce6d-4fd3-891b-58f9e5d70ffe" />


---

## 🏗 Architecture
[Client] -> [FastAPI Gateway] -> [Redis Queue] -> [KEDA Autoscaler] -> [Kubernetes Worker Pods]

* **Ingestion:** Asynchronous FastAPI service handles non-blocking uploads.
* **Buffering:** Redis acts as a decoupled message broker to prevent data loss.
* **Intelligence:** KEDA monitors Redis list length and scales workers.
* **Processing:** Python workers process audio streams and shut down when idle (Scale-to-Zero).

## 🛠 Tech Stack
* **Infrastructure:** Kubernetes (Minikube), Docker
* **Orchestration:** KEDA (Event-Driven Scaling)
* **Backend:** Python, FastAPI, Redis
* **Observability:** Prometheus & Grafana (Custom Dashboards)

## 🚀 How to Run Locally

1. **Start Minikube**
   ```bash
   minikube start --driver=




   Deploy Components

Bash

kubectl apply -f k8s/
Verify Autoscaling Flood the queue and watch KEDA activate:

Bash

kubectl get pods -w
