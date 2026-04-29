from dataclasses import dataclass


@dataclass
class PurchaseCategorizer:
    def categorize_item(self, item_name: str) -> str:
        if not item_name:
            return "unknown"

        name = item_name.lower()

        # Drinks
        if any(w in name for w in [
            "coffee", "latte", "espresso", "cappuccino",
            "tea", "juice", "soda", "water"
        ]):
            return "drink"

        # Meals (main dishes)
        if any(w in name for w in[
            "chicken", "fish", "salad", "burger", "sandwich",
            "pasta", "spaghetti", "bowl", "rice", "entree", "meal"
        ]):
            return "meal"

        # Sides
        if any(w in name for w in[
            "fries", "side", "fruit", "potatoes", "mac and cheese", "banana", "breadstick"
        ]):
            return "side"

        # Snacks
        if any(w in name for w in[
            "chips", "cookie", "brownie", "granola", "bar"
        ]):
            return "snack"

        # Desserts
        if any(w in name for w in[
            "cake", "ice cream", "dessert", "pastry", "milkshake", "shake"
        ]):
            return "dessert"

        return "other"