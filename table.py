# Python program to create a table

from tkinter import *
import csv

list_file = 'qna_pool.csv'

class Table:
	
	def __init__(self,root):
		
		# code for creating table
		for i in range(total_rows):
			for j in range(total_columns):
				
				self.e = Entry(root, width=20, fg='black',
							font=('Arial',16))
				
				self.e.grid(row=i, column=j)
				self.e.insert(END, lst[i][j])
def get_file(list_file):
    global row_count
    global file_error
    try:
        ''' call with file and get back list of lists'''
        with open(list_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            rowlist = []
            questions_list = []
            line_count = 0
            for row in csv_reader:
                if line_count > 0:
                    # avoids the header line
                    rowlist = [row[0]] # initalizes the list
                    rowlist.append(row[1])
                    rowlist.append(row[2])
                    rowlist.append(row[3])
                    questions_list.append(rowlist)
                    # this is a 0 based list of lists
                    # access questions_list[q# - 1][column]
                line_count += 1
            #print(f'Processed {line_count} lines.')
            row_count = line_count - 1
            return [questions_list]
    except FileNotFoundError:
        print('qna_pool.csv data file not found')
        # print message on screen
        file_error = True


# take the data
lst = [('Question','Right','Wrong A','Wrong B'),
	(2,'Aaryan','Pune',18),
	(3,'Vaishnavi','Mumbai',20),
	(19,'Rachna','Mumbai',21),
	(5,'Shubham','Delhi',21)]

try:
    [questions] = get_file(list_file)
except:
    print('FILE IS MISSING')
    #once this is inside a loop ADD BREAK 
# find total number of rows and
# columns in list
print(questions)

total_rows = len(lst)
total_columns = len(lst[0])

# create root window
root = Tk()
t = Table(root)
root.mainloop()
