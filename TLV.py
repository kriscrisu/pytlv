#!/usr/bin/env python

import binascii
from collections import OrderedDict

def hexify(number):
	"""
	Convert integer to hex string representation, e.g. 12 to '0C'
	"""
	result = hex(number).replace('0x', '').upper()
	if divmod(len(result), 2)[1] == 1:
		# Padding
		result = '0{}'.format(result)
	return result


class TLV:

	def __init__(self, tags):
		self.tags = tags
		self.tlv_string = ''
		
		self.tag_lengths = set()
		for tag in self.tags:
			self.tag_lengths.add(len(tag))


	def parse(self, tlv_string):
		"""
		"""
		parsed_data = OrderedDict()
		self.tlv_string = tlv_string

		i = 0
		while i < len(self.tlv_string): 
			tag_found = False

			for tag_length in self.tag_lengths:
				for tag in self.tags:
					if self.tlv_string[i:i+tag_length] == tag:
						value_length = int(self.tlv_string[i+tag_length:i+tag_length+2], 16)

						value_start_position = i+tag_length+2
						value_end_position = i+tag_length+2+value_length*2

						value = self.tlv_string[value_start_position:value_end_position]
						parsed_data[tag] = value

						i = value_end_position
						tag_found = True

			if not tag_found:
				raise ValueError('Unkown tag')
		return parsed_data


	def build(self, data_dict):
		self.tlv_string = ''
		for tag, value in data_dict.items():
			self.tlv_string = self.tlv_string + tag.upper() + hexify(len(value)) + value.upper()

		return self.tlv_string
