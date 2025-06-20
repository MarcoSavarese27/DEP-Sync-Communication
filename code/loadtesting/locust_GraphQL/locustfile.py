from locust import HttpUser, task
import json
from uuid import uuid4


class GraphQLUser(HttpUser):

    @task(3)
    def get_all_products(self):
        query = """
        query {
            getAllProducts {
                id
                uuid
                name
                weight
            }
        }
        """
        self.client.post(
            "/graphql",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"query": query}),
        )

    @task(3)
    def get_product_by_uuid(self):
        query = f"""
        query {{
            getProductByUuid(uuid: "171f5df0-b213-4a40-8ae6-fe82239ab660") {{
                id
                uuid
                name
                weight
            }}
        }}
        """
        self.client.post(
            "/graphql",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"query": query}),
        )
        
    @task(1)
    def add_product(self):
        name = "Kiwi"
        weight = 12.5
        uuid = uuid4()

        mutation = f"""
        mutation {{
            addProduct(name: "{name}", weight: {weight}, uuid: "{uuid}") {{
                id
                uuid
                name
                weight
            }}
        }}
        """
        self.client.post(
            "/graphql",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"query": mutation}),
        )

        mutation = f"""
        mutation {{
            deleteProduct(uuid: "{uuid}") {{
                id
                uuid
                name
                weight
            }}
        }}
        """
        self.client.post(
            "/graphql",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"query": mutation}),
        )
