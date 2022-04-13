import PySimpleGUI as sg
from sparql_query import SPARQLQuery
from pyparsing import ParseException

class SPARQLGUI:

	def __init__(self):
		sg.theme('DarkAmber')   # Add a touch of color
		self.font = ("Courier New", 12) # Extra font to use
		self.sq = SPARQLQuery()
		# results = sq.run_query(sq.graph)
		# sq.write_results(results)
		self.main_window()

	def display_output(self, output):
		layout = [  [sg.Multiline(key = 'results', size=(110,30), autoscroll=True, auto_refresh=True, disabled=True, expand_x=True, expand_y=True)],
					[sg.Text('Output Filename:', size=(15, 1)), sg.InputText('', key='filename')],
					[sg.Button('Save'), sg.Button('Close')] ]
		window = sg.Window('SPARQL Query Output', layout, resizable=True, finalize=True)
		window['results'].print('\n'.join([': '.join(["     " if i is None or not hasattr(i, 'value') else str(i.value) for i in row]) for row in output]))
		# choice = None
		while True:
			event, values = window.read()
			if event == 'Save' and values['filename']:
				self.sq.write_results(values['filename'], output)
				self.notification_window()
				continue
			if event == sg.WIN_CLOSED or event == 'Close':
				break
		window.close()

	def notification_window(self):
		small_layout = [  [sg.Text('Your file has been saved') ],
					[sg.Button('Ok')] ]
		window = sg.Window('', small_layout)
		while True: 
			event, values = window.read()
			if event == sg.WIN_CLOSED or event == 'Ok':
				window.close()
				break

	def main_window(self):
		# All the stuff inside the window.
		right_click_menu = ['', ['Copy', 'Paste', 'Select All'] ]
		layout = [  [sg.Text('Enter your test query here:')],
					[sg.Multiline(size=(110, 30), enter_submits=False, key='query', font=self.font, right_click_menu=right_click_menu)],
					[sg.Button('Output'), sg.Button('Cancel')] ]
		window = sg.Window('SPARQL Query Testing Interface', layout)
		mline:sg.Multiline = window['query']
		# Event Loop to process "events" and get the "values" of the inputs
		while True:
			event, values = window.read()
			if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
				break
			elif event == 'Output':
				try:
					print('You entered:\n', values['query'])
					results = self.sq.run_query(self.sq.graph, values['query'])
					self.display_output(results)
				except ParseException:
					print('You must enter a query.')
			elif event == 'Copy':
				try:
					text = mline.Widget.selection_get()
					window.TKroot.clipboard_clear()
					window.TKroot.clipboard_append(text)
				except:
					print('Nothing selected')
			elif event == 'Paste':
				mline.Widget.insert(sg.tk.INSERT, window.TKroot.clipboard_get())
			elif event == 'Select All':
				mline.Widget.selection_clear()
				mline.Widget.tag_add('sel', '1.0', 'end')
		window.close()

if __name__ == "__main__":
	SPARQLGUI()
	# sg.main_sdk_help()


'''
SELECT  ?title ?price
WHERE   { 
	?x ns:price ?price .
	FILTER (?price < 501)
	?x dc:title ?title . 
}
'''