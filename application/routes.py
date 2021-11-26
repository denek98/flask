from flask import current_app as app
from . import gsheet
from flask import send_file

@app.route('/read-data-from-sheet')
def read_data_from_sheet():
	gsheet_object = gsheet.Gsheet()
	gsheet_object.export_readed_data_to_csv()
	return send_file(gsheet_object.datafile, as_attachment=True)

@app.route('/upload-new-data-to-sheet')
def upload_new_data_to_sheet():
	gsheet_object = gsheet.Gsheet()
	try:
		gsheet_object.upload_new_data_to_sheet()
		return ('New data successfully appended')
	except:
		return('Something went wrong')
