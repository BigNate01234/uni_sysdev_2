import tkinter as tk
from tkinter import ttk
from DatabaseHandler import DatabaseHandler


class ViewSalesMenu:
    """
    Displays the sales that have been completed.
    """
    def __init__(self):
        root = tk.Tk()
        root.geometry('1200x500')
        root.title('Sales')
        label = tk.Label(root, text='Sales', font=('arial', 20))
        label.pack(padx=10, pady=10)

        self.dbh = DatabaseHandler()

        # make the table
        self.table = ttk.Treeview(root,
                                  columns=('saleid', 'itemid', 'date'),
                                  show='headings')
        self.table.heading('itemid', text='Item ID')
        self.table.heading('date', text='Transaction Date')
        self.table.heading('saleid', text='Sale ID')
        self.table.pack(fill='both', expand=True)
        self.refreshTableContent()

        cancelSaleButton = tk.Button(root,
                                     text='Cancel Sale',
                                     font=('arial', 16),
                                     command=self.cancelSale)
        cancelSaleButton.pack(fill='x')

        root.mainloop()

    def refreshTableContent(self):
        data = self.dbh.execute_query('SELECT * FROM Sales ORDER BY id ASC;')

        # delete everything from the table
        for row in self.table.get_children():
            self.table.delete(row)

        # insert the data into the table
        for row in data:
            print(row)
            self.table.insert(parent='', index=0, values=row)

    def cancelSale(self):
        selected_item = self.table.item(self.table.selection())['values']

        sql = 'UPDATE Stock SET quantity={quantity} WHERE id={id};'
        print("selected_item",str(selected_item))
        query = sql.format(quantity=int(selected_item[1])+1, id=selected_item[0])
        self.dbh.execute_query(query)

        query = 'DELETE FROM sales WHERE id={id};'.format(id=selected_item[1])
        self.dbh.execute_query(query)

        self.dbh.commit_changes()
        self.refreshTableContent()


if __name__ == "__main__":
    ViewSalesMenu()
