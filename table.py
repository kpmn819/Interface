# Python program to create a table

from tkinter import *
import csv

list_file = 'qna_pool.csv'

class Table:
	
	def __init__(self,root):
		
		# code for creating table
		for i in range(total_rows):
			for j in range(total_columns):
				
				self.e = Entry(root, width=50, fg='black',
							font=('Arial',10))
				
				self.e.grid(row=i, column=j)
				# row and col index
				#self.e.insert(END, lst_org[i][j])
				self.e.insert(END, q_list[i][j])


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




try:
    [q_list] = get_file(list_file)
except:
    print('FILE IS MISSING')
    #once this is inside a loop ADD BREAK 
# find total number of rows and
# columns in list




total_rows = len(q_list)
total_columns = len(q_list[0])
# create root window
root = Tk()
t = Table(root)
root.mainloop()
