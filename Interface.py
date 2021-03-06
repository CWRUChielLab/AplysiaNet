from tkinter import *

class Interface:

    # The constructor. Currently, only standard mode is supported.
    def __init__(self, master):

        self.status = 'running'

        # Titles the main window
        self.master = master
        master.title('Aplysia Feeding Circuit Simulation')

        # Displays all of the initial text
        self.label0 = Label(master, text='Input: Please enter values between 0 and 8.5.')
        self.label0.grid(row=0, columnspan=3, sticky=W)
        self.label1 = Label(master, text='Please enter values between -10 and 10 for best results.')
        self.label1.grid(row=0, column=3, columnspan=2, sticky=W)
        self.label2 = Label(master, text='Chemical stimulus start:')
        self.label2.grid(row=1, columnspan=1, sticky=W)
        self.label3 = Label(master, text='Chemical stimulus end:')
        self.label3.grid(row=2, columnspan=1, sticky=W)
        self.label4 = Label(master, text='Mechanical stimulus start:')
        self.label4.grid(row=3, columnspan=1, sticky=W)
        self.label5 = Label(master, text='Mechanical stimulus end:')
        self.label5.grid(row=4, columnspan=1, sticky=W)
        self.label6 = Label(master, text='Chemical stimulus current:')
        self.label6.grid(row=1, column=3, columnspan=1, sticky=W)
        self.label7 = Label(master, text='Mechanical stimulus current:')
        self.label7.grid(row=3, column=3, columnspan=1, sticky=W)
        self.error_label1 = Label(master)
        self.error_label2 = Label(master)
        self.error_label3 = Label(master)
        self.error_label4 = Label(master)

        # Sets up the text entry fields
        self.chem_start_entry = Entry(master)
        self.chem_end_entry = Entry(master)
        self.mech_start_entry = Entry(master)
        self.mech_end_entry = Entry(master)
        self.chem_start_entry.grid(row=1, column=2, columnspan=1, sticky=W + E)
        self.chem_end_entry.grid(row=2, column=2, columnspan=1, sticky=W + E)
        self.mech_start_entry.grid(row=3, column=2, columnspan=1, sticky=W + E)
        self.mech_end_entry.grid(row=4, column=2, columnspan=1, sticky=W + E)

        # Sets up the current injection boxes
        self.chem_current_entry = Entry(master)
        self.mech_current_entry = Entry(master)
        self.chem_current_entry.grid(row=1, column=4, columnspan=1, sticky=W + E)
        self.mech_current_entry.grid(row=3, column=4, columnspan=1, sticky=W + E)

        # Configures the run and close buttons
        self.run_button = Button(master, text='Run', command=self.run)
        self.run_button.grid(row=5, column = 4)
        self.close_button = Button(master, text='Close', command=master.quit)
        self.close_button.grid(row = 5, column = 5)

    # This gets the status of the interface, either 'running' if no valid inputs have been entered or 'complete.'
    def get_status(self):
        return self.status

    # This gets the valid start and end times entered by the user in list form.
    def get_input(self):
        return self.input

    def get_current(self):
        return self.current

    # This will eventually pass the stored input to AplysiaNet. Currently, it prints "running simulation."
    def run(self):
        self.error_label1.grid_forget()
        self.error_label2.grid_forget()
        self.error_label3.grid_forget()
        self.error_label4.grid_forget()
        self.validate()
        print("Running simulation")


    # This method takes in the test in each field and ensures that it is a valid number between 0 and 100.
    # It also checks that start time must be less than or equal to end time.
    def validate(self):
        # If any of the entered inputs are cannot be converted to floats, an error message is displayed,
        # and the screen is reset.

        flag = 0

        try:
            self.chem_start = float(self.chem_start_entry.get())
            self.chem_end = float(self.chem_end_entry.get())
            self.mech_start = float(self.mech_start_entry.get())
            self.mech_end = float(self.mech_end_entry.get())
        except ValueError:
            self.error_label3.config(fg='red')
            self.error_label3.config(text='Bad cast. Please only enter numbers between 0 and 8.5.')
            self.error_label3.grid(row=8, columnspan=3, sticky=W)
            flag = 1

        try:
            self.chem_current = float(self.chem_current_entry.get())
            self.mech_current = float(self.mech_current_entry.get())
        except ValueError:
            self.error_label4.config(fg='red')
            self.error_label4.config(text='Bad cast. Please only enter numbers.')
            self.error_label4.grid(row=9, columnspan=3, sticky=W)
            flag = 1

        # If one pair of inputs is somehow invalid, an error message is displayed, and the screen is reset.
        if self.invalid(self.chem_start, self.chem_end) or self.invalid(self.mech_start, self.mech_end) or flag:
            self.reset()

        # If everything is valid, the simulation can continue running.
        else:
            self.status = 'complete'
            self.input = [self.chem_start, self.chem_end, self.mech_start, self.mech_end]
            self.current = [self.chem_current, self.mech_current]
            return

    # This method returns true if the given pair of inputs is invalid or false otherwise. It also shows error messages.
    def invalid(self, start, end):
        # The flag will become 1 if any error is present. This allows the display of multiple error messages at once.
        flag = 0

        # Checks if start is after end
        if start > end:
            self.error_label1.config(fg='red')
            self.error_label1.config(text = 'Invalid value. Start must be less than or equal to end.')
            self.error_label1.grid(row=6, columnspan=3, sticky=W)
            flag = 1

        # Checks if either input is below 0 or avove 8.5
        if start < 0 or start > 8.5 or end < 0 or end > 8.5:
            self.error_label2.config(fg = 'red')
            self.error_label2.config(text = 'Out of bounds. Please only enter values between 0 and 8.5.', )
            self.error_label2.grid(row=7, columnspan=3, sticky=W)
            flag = 1

        # If errors are present, return true, else return false
        if flag:
            return True
        return False

    # This method removes the entered values from the screen
    def reset(self):
        self.chem_start_entry.delete(0, 'end')
        self.chem_end_entry.delete(0, 'end')
        self.mech_start_entry.delete(0, 'end')
        self.mech_end_entry.delete(0, 'end')
        self.chem_current_entry.delete(0, 'end')
        self.mech_current_entry.delete(0, 'end')
        return