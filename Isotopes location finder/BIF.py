#!/usr/bin/python3

import numpy as np
import struct
import pdb


CHAR=1
SHORT=2
INT=4
FLOAT=4


ISOTOPE_NONE=0
COMPTON=1
CAI=2
DETECTED=4
SELECTED=8

IMAGE_FLAG=1
ISOTOPES_FLAG=2

class BIFReader(object):

	def __init__(self, bif_filename):
		# This BIF file reader will read 
		self._bif_filename = bif_filename

		self._version_number = None
		self._distance = None
		self._cai_or_compton = None
		self._num_counts_in_image = None
		self._x_bins = None
		self._y_bins = None
		self._raw_compton_image = None
		self._raw_cai_image = None

		self._has_cai = False
		self._has_compton = False

		self._process_bif_file()

	def _process_bif_file(self):
		
		with open(self._bif_filename, 'rb') as raw_bif:
			self._get_header_info(raw_bif)

			image_flag_raw = raw_bif.read(CHAR)
			image_flag = ord(struct.unpack("c", image_flag_raw)[0])

			if image_flag == IMAGE_FLAG:
				self._get_rad_image(raw_bif)
			
			elif image_flag == ISOTOPES_FLAG:
				self._get_isotopes(raw_bif)


	def _get_isotopes(self, raw_bif):
		raw_number_of_isotopes = raw_bif.read(CHAR)
		number_of_isotopes = ord(struct.unpack("c", raw_number_of_isotopes)[0])

		for isotope in range(number_of_isotopes):
			raw_length_of_isotope_name = raw_bif.read(CHAR)
			length_of_isotope_name = ord(struct.unpack("c", raw_length_of_isotope_name)[0])

			# pdb.set_trace()

			raw_name = raw_bif.read(length_of_isotope_name)

	def _compton_or_cai(self, raw_bif):

		cai_or_compton_raw = raw_bif.read(CHAR)
		tmp_var = ord(struct.unpack("c", cai_or_compton_raw)[0])

		if tmp_var == COMPTON:
			return False
		elif tmp_var == CAI:
			return True
	
	def _get_header_info(self, raw_bif):

		header_flag_raw = raw_bif.read(CHAR)
		header_flag = struct.unpack("c", header_flag_raw)[0]
		

		version_number_raw = raw_bif.read(CHAR)
		self._version_number = struct.unpack("c", version_number_raw)[0]

		string = "H3D, Inc. Binary Image File"
		dumb_string = raw_bif.read(len(string) + 1)

		filename_length_raw = raw_bif.read(SHORT)
		filename_length = struct.unpack("h", filename_length_raw)[0]

		filename = raw_bif.read(filename_length)

		distance_raw = raw_bif.read(FLOAT)
		self._distance = struct.unpack("f", distance_raw)[0]

		extra_crap_raw = raw_bif.read(INT)
		extra_crap = struct.unpack("I", extra_crap_raw)[0]

		_ = raw_bif.read(extra_crap)


	def _get_rad_image(self, raw_bif):

		is_it_a_cai_image = self._compton_or_cai(raw_bif)
		num_counts_in_image_raw = raw_bif.read(INT)
		self._num_counts_in_image = struct.unpack("I", num_counts_in_image_raw)[0]

		x_bins_raw = raw_bif.read(INT)
		self._x_bins = struct.unpack("I", x_bins_raw)[0]

		y_bins_raw = raw_bif.read(INT)
		self._y_bins = struct.unpack("I", y_bins_raw)[0]

		
		this_image =  np.zeros((self._y_bins, self._x_bins))
		for y in range(self._y_bins):
			for x in range(self._x_bins):
				image_bin_val_raw = raw_bif.read(FLOAT)
				image_bin = struct.unpack('f', image_bin_val_raw)[0]
				this_image[y][x] = image_bin
				
		if is_it_a_cai_image:
			self._raw_cai_image = this_image
			self._has_cai = True
		else:
			self._raw_compton_image = this_image
			self._has_compton = True

		## Now need to see if there is another image, also check the compton or cai flag to set the image to the correct variable.


	@property
	def x_bins(self):
		return self._x_bins

	@property
	def y_bins(self):
		return self._y_bins

	@property
	def num_counts_in_image(self):
		return self._num_counts_in_image

	@property
	def distance(self):
		return self.distance

	@property
	def cai_or_compton(self):
		return self._cai_or_compton

	@property
	def compton(self):
		return self._raw_compton_image

	@property
	def cai(self):
		return self._raw_cai_image

	@property
	def has_compton(self):
		return self._has_compton

	@property
	def has_cai(self):
		return self._has_cai