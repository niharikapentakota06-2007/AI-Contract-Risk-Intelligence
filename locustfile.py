import os
from locust import HttpUser, task, between

class APIPerformanceUser(HttpUser):
    # Simulate user wait time between requests (1 to 3 seconds)
    wait_time = between(1, 3)

    @task(3)
    def check_health(self):
        """Simulate frequent load balancer health checks."""
        self.client.get("/health")

    @task(1)
    def upload_and_poll_document(self):
        """Simulate end-to-end user workflow: Upload contract and check status."""
        # Create a dummy file payload
        file_payload = {
            'file': ('sample_contract.pdf', b'Dummy contract text payload for load testing', 'application/pdf')
        }
        
        # 1. Post upload request
        response = self.client.post("/upload", files=file_payload)
        
        if response.status_code == 200:
            task_id = response.json().get("task_id")
            if task_id:
                # 2. Poll the status endpoint for the processing result
                self.client.get(f"/tasks/{task_id}")
