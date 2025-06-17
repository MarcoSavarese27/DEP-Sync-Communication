from product_repository import ProductRepository

class ProductService:
    def __init__(self):
        self.repository = ProductRepository()

    def get_all_products(self):
        return self.repository.get_all_products()

    def get_product_by_uuid(self, uuid: str):
        return self.repository.get_product_by_uuid(uuid)

    def add_product(self, name: str, weight: float):
        return self.repository.add_product(name, weight)

    def delete_product(self, id: int):
        return self.repository.delete_product(id)

