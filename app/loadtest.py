from locust import HttpUser, task, between
import random
import string

# Global dictionary to store keys and values
key_store = {}

class CacheServiceUser(HttpUser):
    wait_time = between(1, 2)  # Simulate user wait time between tasks

    def generate_random_string(self, length=10):
        """Helper function to generate a random string of specified length."""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    def store_key_value(self, key, value):
        """Store the key-value pair in the global dictionary."""
        key_store[key] = value
    
    def update_key_value(self, key):
        """Update an existing key's value in the global dictionary."""
        if key in key_store:
            new_value = self.generate_random_string()
            key_store[key] = new_value
            print(f"Updated key: {key} with new value: {new_value}")

    @task(1)
    def put_key(self):
        """Simulate a request to the /put endpoint to cache a key-value pair."""
        key = self.generate_random_string()
        value = self.generate_random_string()
        response = self.client.post("/put", json={"key": key, "value": value})
        
        if response.status_code == 200:
            self.store_key_value(key, value)
            print(f"Put key: {key} with value: {value}")
        else:
            print(f"Failed to put key: {key} - Status Code: {response.status_code}, Response: {response.text}")

        # Occasionally, update an existing key's value
        if random.random() < 0.2 and key_store:  # 20% chance to update a key
            random_key = random.choice(list(key_store.keys()))
            self.update_key_value(random_key)

    @task(2)
    def get_key(self):
        """Simulate a request to the /get endpoint to retrieve a value by key."""
        if key_store and random.random() < 0.8:  # 80% chance to use an existing key
            key = random.choice(list(key_store.keys()))
            expected_value = key_store[key]
        else:
            key = self.generate_random_string()  # 20% chance to get a random (likely missing) key
            expected_value = None
        
        response = self.client.get(f"/get?key={key}")
        
        if response.status_code == 200:
            response_value = response.json().get("value")
            if response_value == expected_value:
                print(f"Retrieved correct value for key: {key}")
            else:
                print(f"Value mismatch for key: {key}. Expected: {expected_value}, Got: {response_value}")
        elif response.status_code == 404:
            print(f"Key: {key} not found (expected: miss)")
        else:
            print(f"Failed to get key: {key} - Status Code: {response.status_code}, Response: {response.text}")

    @task(3)
    def health_check(self):
        """Simulate a health check request to the /health endpoint."""
        response = self.client.get("/health")
        
        if response.status_code == 200:
            print("Health check passed")
        else:
            print(f"Health check failed - Status Code: {response.status_code}, Response: {response.text}")
