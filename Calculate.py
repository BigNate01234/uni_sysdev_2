import tkinter as tk
from DatabaseHandler import DatabaseHandler


class CalculatePayments:
    """
    A simple form used to calculate how much commision is owed to a band.
    """
    def __init__(self):
        # Setup window
        self.root = tk.Tk()
        self.root.geometry('500x500')
        self.root.title('Calculate Payments')

        # Header
        headerLabel = tk.Label(self.root,
                               text='Payment Calculator',
                               font=('arial', 20))
        headerLabel.pack(padx=10, pady=10)

        # Instruction
        instructionLabel = tk.Label(self.root,
                                    text='Enter a band Name',
                                    font=('arial', 14))
        instructionLabel.pack(padx=10, pady=10)

        # Setup textbox
        self.bandNameText = tk.Entry(self.root, font=('arial', 14))
        self.bandNameText.insert(tk.END, '')
        self.bandNameText.pack(padx=10, pady=10, fill='x')

        # Create button
        calculateButton = tk.Button(self.root,
                                    text='Calculate ammount owed',
                                    font=('arial', 14),
                                    command=self.showCommision)
        calculateButton.pack(padx=10, pady=10, fill='x')

        # Instruction
        self.resultLabel = tk.Label(self.root, text='',  font=('arial', 14))
        self.resultLabel.pack(padx=10, pady=10)

        # Setup connection to db
        self.dbh = DatabaseHandler()

        self.root.mainloop()

    def showCommision(self):
        groupName = self.bandNameText.get()
        sql = """SELECT sum(price) FROM Sales, Stock
        WHERE Sales.itemid=Stock.id AND Stock.musicGroup="{groupName}";
        """.format(groupName=groupName)
        data = self.dbh.execute_query(sql)
        salesVolume = data[0][0]
        if salesVolume is not None:
            commision = salesVolume * 0.25
            self.resultLabel.config(text='Ammount owed: £'+str(commision))
        else:
            self.resultLabel.config(text='Could not find sale for'+groupName)


if __name__ == '__main__':
    CalculatePayments()
