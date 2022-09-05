#	pylzstr - Native Python implementation of LZString string compression
#	Copyright (C) 2022-2022 Johannes Bauer
#
#	This file is part of pylzstr.
#
#	pylzstr is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	pylzstr is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with pylzstr; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>

import enum
from .BitString import BitString
from .Exceptions import LZStringDecompressionException

class SpecialTokens(enum.IntEnum):
	LiteralByte = 0
	LiteralWord = 1
	EndOfStream = 2

class LZStringDecompressor():
	def __init__(self, bs: BitString):
		self._bs = bs
		self._result = None

	def decompress(self):
		if self._result is not None:
			return self._result

		self._bs.seek(0)
		cdict = { i: None for i in range(3) }

		self._result = bytearray()
		last_data = None
		while True:
			token_bits = len(cdict).bit_length()
			token = self._bs.read_bits(token_bits)
			if token in [ SpecialTokens.LiteralByte, SpecialTokens.LiteralWord ]:
				data = bytes(self._bs.read_chars(token + 1))
				cdict[len(cdict)] = data
			elif token == SpecialTokens.EndOfStream:
				return self._result
			else:
				if token in cdict:
					data = cdict[token]
				elif token == len(cdict):
					data = last_data + bytearray([ last_data[0] ])
				else:
					raise LZStringDecompressionException(f"token {token} is not in compression dictionary: {cdict}")

			self._result += data
			if last_data is not None:
				cdict[len(cdict)] = bytes(last_data + bytes([ data[0] ]))
			last_data = data

class LZStringCompressor():
	def __init__(self, data: bytes):
		self._data = data
		self._numbits = 2
		self._enlargein = 2
		self._w = None
		self._cdict = { }
		self._created_dict_for = set()
		self._result = None

	def _produce_w(self):
		if self._w not in self._created_dict_for:
			self._created_dict_for.add(self._w)
			if len(self._w) == 1:
				self._result.append_value(0, self._numbits)
				self._result.append_value(self._w[0], 8)
			else:
				self._result.append_value(1, self._numbits)
				self._result.append_value(self._w[0], 8)
				self._result.append_value(self._w[1], 8)
			self._enlarge_step()
		else:
			self._result.append_value(self._cdict[self._w], self._numbits)
		self._enlarge_step()

	def _enlarge_step(self):
		self._enlargein -= 1
		if self._enlargein == 0:
			self._enlargein = 1 << self._numbits
			self._numbits += 1

	def compress(self):
		if self._result is not None:
			return self._result

		self._result = BitString()
		self._w = b""
		self._cdict = { }
		for char in self._data:
			char = bytes([ char ])
			if char not in self._cdict:
				self._cdict[char] = len(self._cdict)

			wc = self._w + char
			if wc in self._cdict:
				self._w = wc
			else:
				self._produce_w()
				self._cdict[wc] = len(self._cdict)
				self._w = char

		if self._w != b"":
			self._produce_w()

		self._result.append_value(2, self._numbits)
		return self._result
