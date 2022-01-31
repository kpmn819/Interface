from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from tkinter import colorchooser
from configparser import ConfigParser
''' this is some very slick code creates, readsa and writes
to a database'''
''' I have reused some code so the table names don't match
what's going on in the program so First Name = Question
Second Name = Right answer, Address = Wrong A, City = Wrong B'''
root = Tk()
root.title('Codemy.com - TreeBase')
#root.iconbitmap('c:/gui/codemy.ico')
root.geometry("1500x550")

# Read our config file and get colors
parser = ConfigParser()
parser.read("treebase.ini")
saved_primary_color = parser.get('colors', 'primary_color')
saved_secondary_color = parser.get('colors', 'secondary_color')
saved_highlight_color = parser.get('colors', 'highlight_color')

def query_database():
	# Clear the Treeview
	for record in my_tree.get_children():
		my_tree.delete(record)
		
	# Create a database or connect to one that exists
	conn = sqlite3.connect('questions_new.db')

	# Create a cursor instance
	c = conn.cursor()

	c.execute("SELECT rowid, * FROM questions")
	records = c.fetchall()
	
	# Add our data to the screen
	global count
	count = 0
	
	#for record in records:
	#	print(record)


	for record in records:
		# even and odd row color
		if count % 2 == 0:
			my_tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[0], record[4], record[5]), tags=('evenrow',))
		else:
			my_tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[0], record[4], record[5]), tags=('oddrow',))
		# increment counter
		count += 1


	# Commit changes
	conn.commit()

	# Close our connection
	conn.close()

def search_records():
	lookup_record = search_entry.get()
	# close the search box
	search.destroy()
	
	# Clear the Treeview
	for record in my_tree.get_children():
		my_tree.delete(record)
	
	# Create a database or connect to one that exists
	conn = sqlite3.connect('questions_new.db')

	# Create a cursor instance
	c = conn.cursor()

	c.execute("SELECT rowid, * FROM questions WHERE question like ?", (lookup_record,))
	records = c.fetchall()
	
	# Add our data to the screen
	global count
	count = 0
	
	#for record in records:
	#	print(record)


	for record in records:
		if count % 2 == 0:
			my_tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[0], record[4], record[5]), tags=('evenrow',))
		else:
			my_tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[0], record[4], record[5]), tags=('oddrow',))
		# increment counter
		count += 1


	# Commit changes
	conn.commit()

	# Close our connection
	conn.close()


def lookup_records():
	global search_entry, search

	search = Toplevel(root)
	search.title("Lookup Records")
	search.geometry("400x200")
	#search.iconbitmap('c:/gui/codemy.ico')

	# Create label frame
	search_frame = LabelFrame(search, text="Question")
	search_frame.pack(padx=10, pady=10)

	# Add entry box
	search_entry = Entry(search_frame, font=("Helvetica", 18))
	search_entry.pack(pady=20, padx=20)

	# Add button
	search_button = Button(search, text="Search Records", command=search_records)
	search_button.pack(padx=20, pady=20)

def primary_color():
	# Pick Color
	primary_color = colorchooser.askcolor()[1]

	# Update Treeview Color
	if primary_color:
		# Create Striped Row Tags
		my_tree.tag_configure('evenrow', background=primary_color)

		# Config file
		parser = ConfigParser()
		parser.read("treebase.ini")
		# Set the color change
		parser.set('colors', 'primary_color', primary_color)
		# Save the config file
		with open('treebase.ini', 'w') as configfile:
			parser.write(configfile)

def secondary_color():
	# Pick Color
	secondary_color = colorchooser.askcolor()[1]
	
	# Update Treeview Color
	if secondary_color:
		# Create Striped Row Tags
		my_tree.tag_configure('oddrow', background=secondary_color)
		
		# Config file
		parser = ConfigParser()
		parser.read("treebase.ini")
		# Set the color change
		parser.set('colors', 'secondary_color', secondary_color)
		# Save the config file
		with open('treebase.ini', 'w') as configfile:
			parser.write(configfile)

def highlight_color():
	# Pick Color
	highlight_color = colorchooser.askcolor()[1]

	#Update Treeview Color
	# Change Selected Color
	if highlight_color:
		style.map('Treeview',
			background=[('selected', highlight_color)])

		# Config file
		parser = ConfigParser()
		parser.read("treebase.ini")
		# Set the color change
		parser.set('colors', 'highlight_color', highlight_color)
		# Save the config file
		with open('treebase.ini', 'w') as configfile:
			parser.write(configfile)

def reset_colors():
	# Save original colors to config file
	parser = ConfigParser()
	parser.read('treebase.ini')
	parser.set('colors', 'primary_color', 'lightblue')
	parser.set('colors', 'secondary_color', 'white')
	parser.set('colors', 'highlight_color', '#347083')
	with open('treebase.ini', 'w') as configfile:
			parser.write(configfile)
	# Reset the colors
	my_tree.tag_configure('oddrow', background='white')
	my_tree.tag_configure('evenrow', background='lightblue')
	style.map('Treeview',
			background=[('selected', '#347083')])
# Add Menu
my_menu = Menu(root)
root.config(menu=my_menu)



# Configure our menu
option_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Options", menu=option_menu)
# Drop down menu
option_menu.add_command(label="Primary Color", command=primary_color)
option_menu.add_command(label="Secondary Color", command=secondary_color)
option_menu.add_command(label="Highlight Color", command=highlight_color)
option_menu.add_separator()
option_menu.add_command(label="Reset Colors", command=reset_colors)
option_menu.add_separator()
option_menu.add_command(label="Exit", command=root.quit)

#Search Menu
search_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Search", menu=search_menu)
# Drop down menu
search_menu.add_command(label="Search", command=lookup_records)
search_menu.add_separator()
search_menu.add_command(label="Reset", command=query_database)

# Add Fake Data
'''
data = [
	["John", "Elder", 1, "123 Elder St.", "Las Vegas"],
	["Mary", "Smith", 2, "435 West Lookout", "Chicago"],
	["Tim", "Tanaka", 3, "246 Main St.", "New York"]
	
]
'''
# Do some database stuff
# Create a database or connect to one that exists
conn = sqlite3.connect('questions_new.db')

# Create a cursor instance
c = conn.cursor()
# Create Table
c.execute("""CREATE TABLE if not exists questions (
	question text,
	right_ans text,
	id integer,
	wrong_a text,
	wrong_b text)
	""")
# Add dummy data to table
'''
for record in data:
	c.execute("INSERT INTO questions VALUES (:question, :right_ans, :id, :wrong_a, :wrong_b)", 
		{
		'question': record[0],
		'right_ans': record[1],
		'id': record[2],
		'wrong_a': record[3],
		'wrong_b': record[4]
		}
		)
'''


# Commit changes
conn.commit()

# Close our connection
conn.close()

# Add Some Style
style = ttk.Style()

# Pick A Theme
style.theme_use('default')

# Configure the Treeview Colors
style.configure("Treeview",
	background="#D3D3D3",
	foreground="black",
	rowheight=25,
	fieldbackground="#D3D3D3")

# Change Selected Color #347083
style.map('Treeview',
	background=[('selected', saved_highlight_color)])

# Create a Treeview Frame
tree_frame = Frame(root)
tree_frame.pack(pady=10)

# Create a Treeview Scrollbar
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# Create The Treeview
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
my_tree.pack()

# Configure the Scrollbar
tree_scroll.config(command=my_tree.yview)

# Define Our Columns
my_tree['columns'] = ("question", "right_ans", "ID", "wrong_a", "wrong_b")
# Format Our Columns
col = 300
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("question", anchor=W, width=col)
my_tree.column("right_ans", anchor=W, width=col)
my_tree.column("ID", anchor=CENTER, width=50)
my_tree.column("wrong_a", anchor=CENTER, width=col)
my_tree.column("wrong_b", anchor=CENTER, width=col)

# Create Headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("question", text="Question", anchor=W)
my_tree.heading("right_ans", text="Right Answer", anchor=W)
my_tree.heading("ID", text="ID", anchor=CENTER)
my_tree.heading("wrong_a", text="Wrong A", anchor=CENTER)
my_tree.heading("wrong_b", text="Wrong B", anchor=CENTER)

# Create Striped Row Tags
my_tree.tag_configure('oddrow', background=saved_secondary_color)
my_tree.tag_configure('evenrow', background=saved_primary_color)

# Add Record Entry Boxes
data_frame = LabelFrame(root, text="Info")
data_frame.pack(fill="x", expand="yes", padx=20)

qu_label = Label(data_frame, text="Question")
qu_label.grid(row=0, column=0, padx=10, pady=10)
qu_entry = Entry(data_frame)
qu_entry.grid(row=0, column=1, padx=10, pady=10, ipadx = 100)

ra_label = Label(data_frame, text="Right Answer")
ra_label.grid(row=0, column=2, padx=10, pady=10)
ra_entry = Entry(data_frame)
ra_entry.grid(row=0, column=3, padx=10, pady=10, ipadx = 100)

id_label = Label(data_frame, text="ID")
id_label.grid(row=0, column=7, padx=10, pady=10)
id_entry = Entry(data_frame)
id_entry.grid(row=0, column=8, padx=10, pady=10)

wa_label = Label(data_frame, text="Wrong A")
wa_label.grid(row=1, column=0, padx=10, pady=10)
wa_entry = Entry(data_frame)
wa_entry.grid(row=1, column=1, padx=10, pady=10, ipadx = 100)

wb_label = Label(data_frame, text="Wrong B")
wb_label.grid(row=1, column=2, padx=10, pady=10)
wb_entry = Entry(data_frame)
wb_entry.grid(row=1, column=3, padx=10, pady=10, ipadx = 100)

# Move Row Up
def up():
	rows = my_tree.selection()
	for row in rows:
		my_tree.move(row, my_tree.parent(row), my_tree.index(row)-1)

# Move Rown Down
def down():
	rows = my_tree.selection()
	for row in reversed(rows):
		my_tree.move(row, my_tree.parent(row), my_tree.index(row)+1)

# Remove one record
def remove_one():
	x = my_tree.selection()[0]
	my_tree.delete(x)

	# Create a database or connect to one that exists
	conn = sqlite3.connect('questions_new.db')

	# Create a cursor instance
	c = conn.cursor()

	# Delete From Database
	c.execute("DELETE from questions WHERE oid=" + id_entry.get())
	


	# Commit changes
	conn.commit()

	# Close our connection
	conn.close()

	# Clear The Entry Boxes
	clear_entries()

	# Add a little message box for fun
	messagebox.showinfo("Deleted!", "Your Record Has Been Deleted!")

# Remove Many records
def remove_many():
	# Add a little message box for fun
	response = messagebox.askyesno("WOAH!!!!", "This Will Delete EVERYTHING SELECTED From The Table\nAre You Sure?!")

	#Add logic for message box
	if response == 1:
		# Designate selections
		x = my_tree.selection()

		# Create List of ID's
		ids_to_delete = []
		
		# Add selections to ids_to_delete list
		for record in x:
			ids_to_delete.append(my_tree.item(record, 'values')[2])

		# Delete From Treeview
		for record in x:
			my_tree.delete(record)

		# Create a database or connect to one that exists
		conn = sqlite3.connect('questions_new.db')

		# Create a cursor instance
		c = conn.cursor()
		

		# Delete Everything From The Table
		c.executemany("DELETE FROM questions WHERE id = ?", [(a,) for a in ids_to_delete])

		# Reset List
		ids_to_delete = []


		# Commit changes
		conn.commit()

		# Close our connection
		conn.close()

		# Clear entry boxes if filled
		clear_entries()

# Remove all records
def remove_all():
	# Add a little message box for fun
	response = messagebox.askyesno("WOAH!!!!", "This Will Delete EVERYTHING From The Table\nAre You Sure?!")

	#Add logic for message box
	if response == 1:
		# Clear the Treeview
		for record in my_tree.get_children():
			my_tree.delete(record)

		# Create a database or connect to one that exists
		conn = sqlite3.connect('questions_new.db')

		# Create a cursor instance
		c = conn.cursor()

		# Delete Everything From The Table
		c.execute("DROP TABLE questions")
			


		# Commit changes
		conn.commit()

		# Close our connection
		conn.close()

		# Clear entry boxes if filled
		clear_entries()

		# Recreate The Table
		create_table_again()

# Clear entry boxes
def clear_entries():
	# Clear entry boxes
	qu_entry.delete(0, END)
	ra_entry.delete(0, END)
	id_entry.delete(0, END)
	wa_entry.delete(0, END)
	wb_entry.delete(0, END)

# Select Record
def select_record(e):
	# Clear entry boxes
	qu_entry.delete(0, END)
	ra_entry.delete(0, END)
	id_entry.delete(0, END)
	wa_entry.delete(0, END)
	wb_entry.delete(0, END)


	# Grab record Number
	selected = my_tree.focus()
	# Grab record values
	values = my_tree.item(selected, 'values')

	# outpus to entry boxes
	qu_entry.insert(0, values[0])
	ra_entry.insert(0, values[1])
	id_entry.insert(0, values[2])
	wa_entry.insert(0, values[3])
	wb_entry.insert(0, values[4])
	
    # Update record
def update_record():
	# Grab the record number
	selected = my_tree.focus()
	# Update record
	my_tree.item(selected, text="", values=(qu_entry.get(), ra_entry.get(), id_entry.get(), wa_entry.get(), wb_entry.get(),))

	# Update the database
	# Create a database or connect to one that exists
	conn = sqlite3.connect('questions_new.db')

	# Create a cursor instance
	c = conn.cursor()

	c.execute("""UPDATE questions SET
		question = :qu,
		right_ans = :ra,
		wrong_a = :wa,
		wrong_b = :wb
		

		WHERE oid = :oid""",
		{
			'qu': qu_entry.get(),
			'ra': ra_entry.get(),
			'wa': wa_entry.get(),
			'wb': wb_entry.get(),
			'oid': id_entry.get(),
		})
	


	# Commit changes
	conn.commit()

	# Close our connection
	conn.close()

	# Clear entry boxes
	qu_entry.delete(0, END)
	ra_entry.delete(0, END)
	id_entry.delete(0, END)
	wa_entry.delete(0, END)
	wb_entry.delete(0, END)



	

# add new record to database
def add_record():
	# Update the database
	# Create a database or connect to one that exists
	conn = sqlite3.connect('questions_new.db')

	# Create a cursor instance
	c = conn.cursor()

	# Add New Record
	c.execute("INSERT INTO questions VALUES (:qu, :ra, :id, :wa, :wb)",
		{
			'qu': qu_entry.get(),
			'ra': ra_entry.get(),
			'id': id_entry.get(),
			'wa': wa_entry.get(),
			'wb': wb_entry.get(),
		})
	

	# Commit changes
	conn.commit()

	# Close our connection
	conn.close()

	# Clear entry boxes
	qu_entry.delete(0, END)
	ra_entry.delete(0, END)
	id_entry.delete(0, END)
	wa_entry.delete(0, END)
	wb_entry.delete(0, END)
	

	# Clear The Treeview Table
	my_tree.delete(*my_tree.get_children())

	# Run to pull data from database on start
	query_database()

def create_table_again():
	# Create a database or connect to one that exists
	conn = sqlite3.connect('questions_new.db')

	# Create a cursor instance
	c = conn.cursor()

	# Create Table
	c.execute("""CREATE TABLE if not exists answers (
		question text,
		right_ans text,
		id integer,
		wrong_a text,
		wrong_b text)
		""")
	
	# Commit changes
	conn.commit()

	# Close our connection
	conn.close()
# Add Buttons
button_frame = LabelFrame(root, text="Commands")
button_frame.pack(fill="x", expand="yes", padx=20)

update_button = Button(button_frame, text="Update Record", command=update_record)
update_button.grid(row=0, column=0, padx=10, pady=10)

add_button = Button(button_frame, text="Add Record", command=add_record)
add_button.grid(row=0, column=1, padx=10, pady=10)

'''remove_all_button = Button(button_frame, text="Remove All Records", command=remove_all)
remove_all_button.grid(row=0, column=2, padx=10, pady=10)'''

remove_one_button = Button(button_frame, text="Remove One Selected", command=remove_one)
remove_one_button.grid(row=0, column=3, padx=10, pady=10)

'''remove_many_button = Button(button_frame, text="Remove Many Selected", command=remove_many)
remove_many_button.grid(row=0, column=4, padx=10, pady=10)'''

'''move_up_button = Button(button_frame, text="Move Up", command=up)
move_up_button.grid(row=0, column=5, padx=10, pady=10)

move_down_button = Button(button_frame, text="Move Down", command=down)
move_down_button.grid(row=0, column=6, padx=10, pady=10)'''

select_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
select_record_button.grid(row=0, column=7, padx=10, pady=10)

# Bind the treeview
my_tree.bind("<ButtonRelease-1>", select_record)

# Run to pull data from database on start
query_database()

root.mainloop()