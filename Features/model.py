from dataclasses import dataclass, asdict

@dataclass
class Item:
    name: str
    quantity: int
    price: float
    category: str

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data):
        return Item(
            name=str(data.get("name", "")),
            quantity=int(data.get("quantity", 0)),
            price=float(data.get("price", 0)),
            category=str(data.get("category", "General"))
        )

@dataclass
class Category:
    name: str

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data):
        if isinstance(data, str):
            return Category(name=data)

        return Category(
            name=str(data.get("name", "General"))
        )