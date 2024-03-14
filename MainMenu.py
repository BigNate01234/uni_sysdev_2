import tkinter as tk
from StockInventory import StockMenu
from SellItems import SellItemsMenu
from Calculate import CalculatePayments
from ViewSalesMenu import ViewSalesMenu


class MainMenu:
    """
    Creates a gui that lets the user access the other parts of the program.
    """
    def __init__(self):

        root = tk.Tk()
        root.geometry('800x500')
        root.title('Main Menu')
        label = tk.Label(root, text='Main menu', font=('arial', 20))
        label.pack(padx=10, pady=10)

        buttonFrame = tk.Frame(root)
        buttonFrame.columnconfigure(0, weight=1)
        buttonFrame.columnconfigure(1, weight=1)

        stockButton = tk.Button(buttonFrame,
                                text='View Stock',
                                font=('arial', 16),
                                command=StockMenu)
        stockButton.grid(row=0, column=0, sticky=tk.W+tk.E)

        viewSalesButton = tk.Button(buttonFrame,
                                    text='View Sales',
                                    font=('arial', 16),
                                    command=ViewSalesMenu)
        viewSalesButton.grid(row=0, column=1, sticky=tk.W+tk.E)

        salesButton = tk.Button(buttonFrame,
                                text='Sell Items',
                                font=('arial', 16),
                                command=SellItemsMenu)
        salesButton.grid(row=1, column=0, sticky=tk.W+tk.E)

        calculateButton = tk.Button(buttonFrame,
                                    text='Calculate Fees',
                                    font=('arial', 16),
                                    command=CalculatePayments)
        calculateButton.grid(row=1, column=1, sticky=tk.W+tk.E)

        buttonFrame.pack(fill='both')

        root.mainloop()


if __name__ == '__main__':
    MainMenu()
