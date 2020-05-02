import json

class FormStructureParser:
	"""
	Gets img data in ndarray format returns dict with parsed ROIs
	"""
	def __init__(self, form_structure_json):
		self.FormStructure = self.load_form_structure(form_structure_json)

	def load_form_structure(self, form_structure_json):
		return json.loads(form_structure_json)

	def process_form (self, form):
		for field in self.FormStructure["fields"]:
			self.process_field(field, form)

	def process_field(self, field, form):
		x = field["topLeft"]["x"]
		width = field["boxWidth"]
		y = field["topLeft"]["y"]
		height = field["boxHeight"]
		return form[x:x+width,y:y+height]


	# def get_question_patch(self, transf, question_index):
	# 	"""Exracts a region of interest (ROI) of a single question."""
	# 	# Top left of question patch q_number
	# 	tl = sheet_coord_to_transf_coord(
	# 		ANSWER_PATCH_LEFT_MARGIN,
	# 		FIRST_ANSWER_PATCH_TOP_Y + ANSWER_PATCH_HEIGHT_WITH_MARGIN * question_index
	# 	)
	# 	# Bottom right of question patch q_number
	# 	br = sheet_coord_to_transf_coord(
	# 		ANSWER_SHEET_WIDTH - ANSWER_PATCH_RIGHT_MARGIN,
	# 		FIRST_ANSWER_PATCH_TOP_Y +
	# 		ANSWER_PATCH_HEIGHT +
	# 		ANSWER_PATCH_HEIGHT_WITH_MARGIN * question_index
	# 	)
	# 	return transf[tl[1]:br[1], tl[0]:br[0]]

if __name__ == "__main__":
	pass
