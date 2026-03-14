from locust import HttpUser, between, task


class TextToSQLUser(HttpUser):
    wait_time = between(1, 2)

    @task(2)
    def health(self):
        self.client.get("/api/v1/health")

    @task(1)
    def query(self):
        payload = {
            "question": "show order totals",
            "session_id": "load-test-session",
            "retrieval_strategy": "mmr",
        }
        self.client.post("/api/v1/query", json=payload)

