from locust import HttpUser, task
import json


class GraphQLUser(HttpUser):

    @task
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

    @task
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
    #def add_product(self):
    #    name = random_name()
    #    weight = round(random.uniform(0.5, 5.0), 2)
    #    mutation = f"""
    #    mutation {{
    #        addProduct(name: "{name}", weight: {weight}) {{
    #            id
    #            uuid
    #            name
    #            weight
    #        }}
    #    }}
    #    """
    #    self.client.post(
    #        "/graphql",
    #        headers={"Content-Type": "application/json"},
    #        data=json.dumps({"query": mutation}),
    #    )
