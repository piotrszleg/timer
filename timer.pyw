import tkinter as tk
import winsound

# Timer app written in python with tkinter
# Author: Piotr Szleg

# Main app window
class Timer(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.pack()

		# init variables
		self.seconds=self.initialSeconds=0
		self.minutes=self.initialMinutes=30
		self.hours=self.initialHours=0
		self.running=False

		self.create_widgets()
		self.updateTime()

	# Creates label and button widgets
	def create_widgets(self):
		self.labelText= tk.StringVar()
		self.label = tk.Label(self, textvariable=self.labelText, font=("Helvetica", 50))
		self.label.pack(side="top")
		self.updateLabel()

		self.buttonLabel=tk.Label(self)
		self.buttonLabel.pack()

		self.pauseButton= tk.Button(self.buttonLabel, text="run", command=self.pause)
		self.pauseButton.pack(side="left")

		self.stopButton= tk.Button(self.buttonLabel, text="stop", command=self.stop)
		self.stopButton.pack(side="left")

		self.setButton= tk.Button(self.buttonLabel, text="set", command=self.set)
		self.setButton.pack(side="left")

		self.dialog=SetTimeDialog(self, self.master)

	# Function called by "run"/"pause" button
	def pause(self):
		self.running=not self.running
		self.updatePauseButton()

	# Function called by "stop" button
	def stop(self):
		self.running=False

		# revert values back to when they were initially set
		self.seconds=self.initialSeconds
		self.minutes=self.initialMinutes
		self.hours=self.initialHours

		self.updateLabel()
		self.updatePauseButton()

	# Function called by "set" button
	def set(self):
		self.running=False

		# update and show SetTimeDialog
		self.dialog.updateEntries()
		self.dialog.pack()

		# Disable normal controls
		self.stopButton["state"]=tk.DISABLED
		self.pauseButton["state"]=tk.DISABLED
		self.setButton["state"]=tk.DISABLED

	# Applies changes from SetTimeDialog and changes application back to normal state
	def applyTime(self):
		self.updateLabel()
		self.updatePauseButton()
		self.stopButton["state"]=tk.NORMAL
		self.pauseButton["state"]=tk.NORMAL
		self.setButton["state"]=tk.NORMAL
		self.dialog.pack_forget()

	# Sets the text on "run"/"pause" button
	def updatePauseButton(self):
		if self.running: 
			self.pauseButton["text"]="pause"
		else: 
			self.pauseButton["text"]="run"

	# Sets the text on the main label depending on current time values
	def updateLabel(self):
		self.labelText.set("{0:02d}:{1:02d}:{2:02d}".format(self.hours, self.minutes, self.seconds))

	# Called every second after first invoking, updates time values
	def updateTime(self):
		if(self.running):
			self.seconds-=1
			if(self.seconds<0):
				self.minutes-=1
				self.seconds=59
				if(self.minutes<0):
					self.minutes=59
					self.hours-=1
					if(self.hours<0):
						# Every time value is <=0, move the window to the top and make beep sound
						self.master.attributes('-topmost', True)
						winsound.Beep(700, 1000)
						# After beep remove -topmost attribute
						self.master.attributes('-topmost', False)
						#stop time
						self.stop()
						
			self.updateLabel()
		# repeat this function every second
		self.after(1000, self.updateTime)

# Input that appears when "set" button is pressed
class SetTimeDialog(tk.Frame):
	def __init__(self, timer, master=None):
		super().__init__(master)
		self.timer=timer
		self.create_widgets()
		self.updateEntries()

	# Creates entry and label widgets
	def create_widgets(self):
		self.hoursEntry=tk.Entry(self, width=2)
		self.hoursEntry.pack(side="left")

		colon=tk.Label(self, text=":")
		colon.pack(side="left")

		self.minutesEntry=tk.Entry(self, width=2)
		self.minutesEntry.pack(side="left")

		colon=tk.Label(self, text=":")
		colon.pack(side="left")

		self.secondsEntry=tk.Entry(self, width=2)
		self.secondsEntry.pack(side="left")

		self.okButton= tk.Button(self, text="ok", command=self.apply)
		self.okButton.pack(side="left")

	# Sets values of entries as current time in Timer
	def updateEntries(self):
		self.hoursEntry.delete(0, tk.END)
		self.hoursEntry.insert(0, "{0:02d}".format(self.timer.hours))
		self.minutesEntry.delete(0, tk.END)
		self.minutesEntry.insert(0, "{0:02d}".format(self.timer.minutes))
		self.secondsEntry.delete(0, tk.END)
		self.secondsEntry.insert(0, "{0:02d}".format(self.timer.seconds))

	# Pushes values to Timer
	def apply(self):
		self.timer.seconds=self.timer.initialSeconds=int(self.secondsEntry.get())
		self.timer.minutes=self.timer.initialMinutes=int(self.minutesEntry.get())
		self.timer.hours  =self.timer.initialHours  =int(self.hoursEntry.get())
		self.timer.applyTime()

# Init application
root = tk.Tk()
root.wm_title("Timer")
app = Timer(master=root)
app.mainloop()
