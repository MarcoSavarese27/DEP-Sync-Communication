from concurrent import futures
import grpc
import uuid
from proto import product_pb2, product_pb2_grpc
from product_repository import ProductRepository

class ProductServiceServicer(product_pb2_grpc.ProductServiceServicer):
    def __init__(self):
        self.repository = ProductRepository()

    def GetAllProducts(self, request, context):
        products = self.repository.get_all_products()
        return product_pb2.ProductList(products=[
            product_pb2.Product(id=p.id, uuid=p.uuid, name=p.name, weight=p.weight)
            for p in products
        ])

    def GetProductByUUID(self, request, context):
        product = self.repository.get_product_by_uuid(request.uuid)
        if product:
            return product_pb2.Product(id=product.id, uuid=product.uuid, name=product.name, weight=product.weight)
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Product not found')
        return product_pb2.Product()

    def AddProduct(self, request, context):
        product = self.repository.add_product(request.name, request.weight)
        return product_pb2.Product(id=product.id, uuid=product.uuid, name=product.name, weight=product.weight)

    def DeleteProduct(self, request, context):
        success = self.repository.delete_product(request.uuid)
        return product_pb2.DeleteResponse(success=success)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    product_pb2_grpc.add_ProductServiceServicer_to_server(ProductServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
