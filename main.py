import tkinter as tk
from Features.repository import InventoryRepository
from Features.service import InventoryService
from Features.view import InventoryView

def main():

    repository = InventoryRepository()
    service = InventoryService(
        repository
    )

    root = tk.Tk()
    InventoryView(
        root,
        service
    )

    root.mainloop()

if __name__ == "__main__":
    main()