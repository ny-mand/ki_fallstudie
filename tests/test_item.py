from src.item import Item
def test_item_erstellung():
    test_item = Item("KI Fallstudie","Gruppenprojekt")
    assert test_item.name == "KI Fallstudie"
    assert test_item.description == "Gruppenprojekt"