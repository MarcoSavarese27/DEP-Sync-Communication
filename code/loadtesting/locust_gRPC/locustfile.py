import grpc
import time
import product_pb2
import product_pb2_grpc
from locust import User, task, events
from uuid import uuid4

class GRPCClient:
    def __init__(self):
        self.channel = grpc.insecure_channel("localhost:8004")
        self.stub = product_pb2_grpc.ProductServiceStub(self.channel)

    def get_all_products(self):
        return self.stub.GetAllProducts(product_pb2.Empty())

    def get_product_by_uuid(self, uuid):
        return self.stub.GetProductByUUID(product_pb2.ProductUUID(uuid=uuid))
    
    def add_product(self, uuid, name, weight):
        return self.stub.AddProduct(
            product_pb2.ProductRequest(name=name, weight=weight, uuid=uuid) 
        )

    def delete_product(self, uuid):
        return self.stub.DeleteProduct(product_pb2.ProductUUID(uuid=uuid))

class GRPCUser(User):
    def on_start(self):
        self.client = GRPCClient()
        try:
            response = self.client.get_all_products()
            self.uuids = [product.uuid for product in response.products]
        except Exception as e:
            print(f"Error during startup UUID fetch: {e}")
            self.uuids = []

    def record_request(self, name, func, *args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            total_time = (time.time() - start_time) * 1000
            events.request.fire(
                request_type="gRPC",
                name=name,
                response_time=total_time,
                response_length=len(result.SerializeToString()) if result else 0
            )
        except Exception as e:
            total_time = (time.time() - start_time) * 1000
            events.request.fire(
                request_type="gRPC",
                name=name,
                response_time=total_time,
                exception=e
            )
            
    @task(3)
    def get_all(self):
        self.record_request("GetAllProducts", self.client.get_all_products)

    @task(3)
    def get_by_uuid(self):
        self.record_request("GetProductByUUID", self.client.get_product_by_uuid, "171f5df0-b213-4a40-8ae6-fe82239ab660")

    @task(1)
    def add_and_delete(self):
        uuid = str(uuid4())
        self.record_request("AddProduct", self.client.add_product, uuid, "Kiwi", 12.5)
        self.record_request("DeleteProduct", self.client.delete_product, uuid)
