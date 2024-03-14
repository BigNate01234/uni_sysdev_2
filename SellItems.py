import tkinter as tk
from tkinter import ttk
from datetime import datetime
from DatabaseHandler import DatabaseHandler


class SellItemsMenu:
    """
    Staff can use this screen to sell items.
    """
    def __init__(self):
        # Setup window
        root = tk.Tk()
        root.geometry('1200x500')
        root.title('Sell Items')
        label = tk.Label(root, text='Sell Items', font=('arial', 20))
        label.pack(padx=10, pady=10)

        # Setup db connection
        self.dbh = DatabaseHandler()

        # Setup Table
        self.table = ttk.Treeview(root,
                                  columns=('id',
                                           'name',
                                           'price',
                                           'quantity',
                                           'musicGroup'),
                                  show='headings')
        self.table.heading('id', text='Item ID')
        self.table.heading('name', text='Name')
        self.table.heading('price', text='Price')
        self.table.heading('quantity', text='Quantity Remaining')
        self.table.heading('musicGroup', text='Music Group')

        self.table.pack(fill='both', expand=True)
        self.refreshTableContent()

        # Add a sell item button
        stockButton = tk.Button(root,
                                text='Sell Selected Item',
                                font=('arial', 16),
                                command=self.sellItem)
        stockButton.pack(fill='x')

        root.mainloop()

    def refreshTableContent(self):
        data = self.dbh.execute_query('SELECT * FROM Stock')

        # delete everything from the table
        for row in self.table.get_children():
            self.table.delete(row)

        # insert the data into the table
        for row in data:
            self.table.insert(parent='', index=row[0], values=row)

    def sellItem(self):
        # if theres more than 0, reduce the number of that item by 1
        selected_item = self.table.item(self.table.selection())['values']
        print(selected_item)

        sql = """UPDATE Stock SET quantity={quantity} WHERE id={id}
        """.format(quantity=selected_item[3]-1, id=selected_item[0])
        self.dbh.execute_query(sql)

        sql = """INSERT INTO Sales (itemid, date) VALUES ({id}, "{date}")
        """.format(id=selected_item[0],
                   date=datetime.now().strftime("%d/%m/%y"))
        self.dbh.execute_query(sql)

        self.dbh.commit_changes()
        self.refreshTableContent()


if __name__ == '__main__':
    SellItemsMenu()
