import tkinter as tk
from tkinter import ttk
from DatabaseHandler import DatabaseHandler


class StockMenu:
    """
    This screen is used to keep track of what items are in stock.
    """
    def __init__(self):
        root = tk.Tk()
        root.geometry('1200x500')
        root.title('Stock Inventory')
        label = tk.Label(root, text='Stock Inventory', font=('arial', 20))
        label.pack(padx=10, pady=10)

        # Setup db
        self.dbh = DatabaseHandler()
        self.dbh.create_tables()

        # make the GUI table
        self.table = ttk.Treeview(root, columns=('id',
                                                 'name',
                                                 'price',
                                                 'quantity',
                                                 'group'), show='headings')
        self.table.heading('id', text='Item ID')
        self.table.heading('name', text='Name')
        self.table.heading('price', text='Price')
        self.table.heading('quantity', text='Quantity Remaining')
        self.table.heading('group', text='Music Group')
        self.table.pack(fill='both', expand=True)

        self.refreshTableContent()
        self.table.bind('<Delete>', self.deleteFromTable)

        # Setup buttons
        buttonFrame = tk.Frame(root)
        buttonFrame.columnconfigure(0, weight=1)
        buttonFrame.columnconfigure(1, weight=1)
        buttonFrame.columnconfigure(2, weight=1)
        buttonFrame.columnconfigure(3, weight=1)

        deleteButton = tk.Button(buttonFrame, text='Delete selected row',
                                 font=('arial', 16),
                                 command=self.deleteFromTable)
        deleteButton.grid(row=0, column=0, sticky=tk.W+tk.E)
        createButton = tk.Button(buttonFrame,
                                 text='Create new row',
                                 font=('arial', 16), command=self.createNew)
        createButton.grid(row=0, column=1, sticky=tk.W+tk.E)
        updateButton = tk.Button(buttonFrame,
                                 text='Update row',
                                 font=('arial', 16),
                                 command=self.launchStockMenu)
        updateButton.grid(row=0, column=2, sticky=tk.W+tk.E)
        refreshButton = tk.Button(buttonFrame,
                                  text='Refresh table',
                                  font=('arial', 16),
                                  command=self.refreshTableContent)
        refreshButton.grid(row=0, column=3, sticky=tk.W+tk.E)

        buttonFrame.pack(fill='both')

        root.mainloop()

    def refreshTableContent(self):
        data = self.dbh.execute_query('SELECT * FROM Stock')

        # delete everything from the table
        for row in self.table.get_children():
            self.table.delete(row)

        # insert the data into the table
        for row in data:
            self.table.insert(parent='', index=row[0], values=row)

    def deleteFromTable(self, *_):
        # delete the item with this id
        item_id = self.table.item(self.table.selection())['values'][0]
        query = 'DELETE FROM Stock WHERE id='+str(item_id)+';'
        self.dbh.execute_query(query)
        self.dbh.commit_changes()

        # then make the thing refresh
        self.refreshTableContent()

    def createNew(self):
        # make a new item in the database with some default values
        query = """ INSERT INTO Stock (name, price, quantity, musicGroup)
                    VALUES ('name',1,1,'default');"""
        self.dbh.execute_query(query)
        self.dbh.commit_changes()
        # then update screen
        self.refreshTableContent()

    def launchStockMenu(self):
        item_id = self.table.item(self.table.selection())['values'][0]
        UpdateMenu(item_id)


class UpdateMenu:

    def __init__(self, item_id):
        self.root = tk.Tk()
        self.root.geometry('800x500')
        self.root.title('Update Item')
        label = tk.Label(self.root, text='Update Item', font=('arial', 20))
        label.pack(padx=10, pady=10)

        # Setup db connection
        self.dbh = DatabaseHandler()
        query = 'SELECT * FROM Stock WHERE id={id};'.format(id=item_id)

        # query the db and unpack tuples
        data = self.dbh.execute_query(query)
        for row in data:
            (id, name, price, quantity, group) = row

        # Create text boxes
        textBoxFrame = tk.Frame(self.root, height=60)
        for x in range(0, 6):
            textBoxFrame.columnconfigure(x, weight=1)

        textBoxFrame.grid_propagate(False)

        idLabel = tk.Label(textBoxFrame, text='Item Id')
        idLabel.grid(row=0, column=0, sticky=tk.W+tk.E, padx=5)
        nameLabel = tk.Label(textBoxFrame, text='Name')
        nameLabel.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5)
        priceLabel = tk.Label(textBoxFrame, text='Price')
        priceLabel.grid(row=0, column=2, sticky=tk.W+tk.E, padx=5)
        quantityLabel = tk.Label(textBoxFrame, text='Quantity Remaining')
        quantityLabel.grid(row=0, column=3, sticky=tk.W+tk.E, padx=5)
        groupLabel = tk.Label(textBoxFrame, text='Music Group')
        groupLabel.grid(row=0, column=4, sticky=tk.W+tk.E, padx=5)

        self.idText = tk.Text(textBoxFrame)
        self.nameText = tk.Text(textBoxFrame)
        self.priceText = tk.Text(textBoxFrame)
        self.quantityText = tk.Text(textBoxFrame)
        self.groupText = tk.Text(textBoxFrame)

        self.idText.grid(row=1, column=0, sticky=tk.W+tk.E, padx=5)
        self.nameText.grid(row=1, column=1, sticky=tk.W+tk.E, padx=5)
        self.priceText.grid(row=1, column=2, sticky=tk.W+tk.E, padx=5)
        self.quantityText.grid(row=1, column=3, sticky=tk.W+tk.E, padx=5)
        self.groupText.grid(row=1, column=4, sticky=tk.W+tk.E, padx=5)

        self.idText.insert(tk.END, str(id))
        self.idText.config(state=tk.DISABLED)
        self.nameText.insert(tk.END, name)
        self.priceText.insert(tk.END, str(price))
        self.quantityText.insert(tk.END, str(quantity))
        self.groupText.insert(tk.END, str(group))

        textBoxFrame.pack(fill='x', pady=10, padx=10)

        # Create buttons
        buttonFrame = tk.Frame(self.root)
        buttonFrame.columnconfigure(0, weight=1)
        buttonFrame.columnconfigure(1, weight=1)

        saveButton = tk.Button(buttonFrame, text='Save and Exit',
                               font=('arial', 16),
                               command=self.saveAndExit)
        saveButton.grid(row=0, column=0, sticky=tk.W+tk.E, padx=10, pady=10)
        exitButton = tk.Button(buttonFrame,
                               text='Exit without saving',
                               font=('arial', 16),
                               command=self.root.destroy)
        exitButton.grid(row=0, column=1, sticky=tk.W+tk.E, padx=10, pady=10)
        buttonFrame.pack(fill='both')

        self.root.mainloop()

    def saveAndExit(self, *_):
        id = self.idText.get("1.0", tk.END).strip()
        name = self.nameText.get("1.0", tk.END).strip()
        quantity = self.quantityText.get("1.0", tk.END).strip()
        price = self.priceText.get("1.0", tk.END).strip()
        group = self.groupText.get("1.0", tk.END).strip()

        fmt_str = """UPDATE Stock
        SET name="{name}",
            price={price},
            quantity={quantity},
            musicGroup="{group}"
        WHERE id={id}"""
        sql = fmt_str.format(name=name,
                             price=price,
                             quantity=quantity,
                             id=id,
                             group=group)

        self.dbh.execute_query(sql)
        self.root.destroy()


if __name__ == '__main__':
    menu = StockMenu()
