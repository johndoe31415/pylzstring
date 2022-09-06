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

	@classmethod
	def decompress_from_bytes(cls, data: bytes):
		bitstring = BitString.from_bytes(data)
		return cls(bitstring).decompress()

	@classmethod
	def decompress_from_base64(cls, b64data: str):
		bitstring = BitString.from_base64(b64data)
		return cls(bitstring).decompress()

	@classmethod
	def decompress_from_url_component(cls, urlcomponent: str):
		bitstring = BitString.from_url_component(urlcomponent)
		return cls(bitstring).decompress()

class LZStringCompressor():
	def __init__(self, data: bytes):
		self._data = data
		self._cdict = None
		self._not_emitted_yet = set()
		self._result = None
		self._dictsize = 3

	@property
	def token_bits(self):
		token_bits = (self._dictsize - 1).bit_length()
		return token_bits

	def _emit(self, pattern: bytes):
		if pattern in self._not_emitted_yet:
			self._not_emitted_yet.remove(pattern)
			self._result.append_value(SpecialTokens.LiteralByte, self.token_bits)
			self._result.append_value(pattern[0], 8)
			self._dictsize += 2
		else:
			self._result.append_value(self._cdict[pattern], self.token_bits)
			self._dictsize += 1

	def compress(self):
		if self._result is not None:
			return self._result

		self._result = BitString()
		self._cdict = { }

		pattern = b""
		for substring in self._data:
			substring = bytes([ substring ])

			if substring not in self._cdict:
				self._not_emitted_yet.add(substring)
				self._cdict[substring] = len(self._cdict) + 3

			combined_pattern = pattern + substring
			if combined_pattern in self._cdict:
				pattern = combined_pattern
			else:
				self._emit(pattern)
				self._cdict[combined_pattern] = len(self._cdict) + 3
				pattern = substring

		if len(pattern) > 0:
			self._emit(pattern)

		self._result.append_value(SpecialTokens.EndOfStream, self.token_bits)
		self._cdict = None
		return self._result

	@classmethod
	def compress_to_bytes(cls, data: bytes):
		bitstring = cls(data).compress()
		return bytes(bitstring)

	@classmethod
	def compress_to_base64(cls, data: bytes):
		bitstring = cls(data).compress()
		return bitstring.to_base64()

	@classmethod
	def compress_to_url_component(cls, data: bytes):
		bitstring = cls(data).compress()
		return bitstring.to_url_component()
