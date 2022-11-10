# MY BUDGET
#### Video Demo:  https://youtu.be/fsLyq4j0Xgc
#### Description:
My Budget is a command-line application to keep track of personal finances. It was built with Python for the final project of the Harvardx course CS50P.

I've decided to store the data on .csv files instead of using a database like SQLite because I wanted to practice the usage of the file reader. 

In the main menu, the user may choose between five options: previous month, next month, add transaction, remove transaction and exit. 

The files of the months are stored inside the year folder. To create the years folders and months files this application uses the [datetime](https://docs.python.org/3/library/datetime.html#date-objects) library.
    
To add a transaction, the user must answer if it is an expense or income. Then, the user must answer the day, add a description and the amount of the transaction. When the files are read, the expenses are formatted as a negative float and all the transactions are summed to generate the month balance.
    
As the files are not supposed to be large, I store the data in a variable when I want to delete a line, then I re-write the file with that line removed.

This application also uses [Colorama](https://pypi.org/project/colorama/) and [Tabulate](https://pypi.org/project/tabulate/) to improve the command-line readability.