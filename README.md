# ML Microservices Platform

This project presents a complete Machine Learning microservices platform designed using modern backend and DevOps practices. The system enables users to authenticate, perform predictions using a trained ML model, and store/retrieve prediction history. The architecture follows a microservices approach and is deployed using Docker and Kubernetes.

## Objectives

* Build a scalable ML-based backend system.
* Implement microservices architecture.
* Integrate authentication using JWT.
* Deploy services using Docker and Kubernetes.
* Provide a simple frontend interface.
* Implement basic monitoring using Prometheus and Grafana.

## Technologies Used

* **Backend**: FastAPI (Python)
* **ML Model**: Scikit-learn
* **Database**: PostgreSQL
* **Containerization**: Docker
* **Orchestration**: Kubernetes (Minikube)
* **Monitoring**: Prometheus, Grafana
* **Frontend**: HTML, CSS, JavaScript

## System Architecture & Services

The system consists of multiple independent services:

* **API Gateway**: Acts as the central entry point for all client requests, handles routing between services, and performs authentication verification.
* **Auth Service**: Handles user registration and login, generating JWT tokens for secure access.
* **ML Service**: Loads the trained machine learning model and provides prediction results based on input data (gender, age, salary).
* **History Service**: Stores prediction results in PostgreSQL and retrieves past predictions.
* **Database**: PostgreSQL is used to store prediction records.
* **Frontend**: A simple interface that allows login, prediction requests, and viewing history.

## Workflow

1. User logs in via frontend.
2. Auth service validates credentials and returns a JWT.
3. User sends a prediction request via API Gateway.
4. Gateway forwards the request to the ML service.
5. ML service returns the prediction.
6. Gateway sends data to the History service.
7. History service stores data in PostgreSQL.
8. User can view prediction history via frontend.

## Features Implemented

* **Authentication**: Secure API access using a JWT-based login system.
* **Prediction System**: Returns predictions and meanings based on gender, age, and salary inputs.
* **Data Storage**: Predictions saved to PostgreSQL with history retrieval supported.
* **Containerization**: Each service is containerized using Docker, with images pushed to Docker Hub.
* **Kubernetes Deployment**: Services deployed using Deployments and Services. Internal communication is handled using ClusterIP, with external access via NodePort and port-forward.
* **Monitoring (Basic)**: Prometheus collects service metrics, and Grafana visualizes system status.

## Future Enhancements

* Add advanced metrics (latency, request tracking).
* Implement role-based authentication.
* Improve frontend using modern frameworks (React).
* Deploy on cloud platforms (AWS/GCP).
* Add a CI/CD pipeline.
