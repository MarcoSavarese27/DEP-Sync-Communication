import strawberry
from typing import List, Optional
from product_model import Product
from product_service import ProductService

product_service = ProductService()
@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_product(self, name: str, weight: float) -> Product:
        return product_service.add_product(name, weight)

    @strawberry.mutation
    def delete_product(self, id: int) -> bool:
        return product_service.delete_product(id)

@strawberry.type
class Query:
    @strawberry.field
    def get_all_products(self) -> List[Product]:
        return product_service.get_all_products()

    @strawberry.field
    def get_product_by_uuid(self, uuid: str) -> Optional[Product]:
        return product_service.get_product_by_uuid(uuid)

schema = strawberry.Schema(query=Query, mutation=Mutation)

