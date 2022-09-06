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

def _swap_bit_order(x: int, bitcount: int = 8):
	y = 0
	for i in range(bitcount):
		if (x & (1 << i)) != 0:
			y |= (1 << (bitcount - 1 - i))
	return y

class BitString():
	_BASE64 = { char: _swap_bit_order(index, 6) for (index, char) in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/") }
	_URI_COMPONENT = { char: _swap_bit_order(index, 6) for (index, char) in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-") }
	_INV_BASE64 = { value: key for (key, value) in _BASE64.items() }
	_INV_URI_COMPONENT = { value: key for (key, value) in _URI_COMPONENT.items() }

	def __init__(self):
		self._bs = bytearray()
		self._bitlen = 0
		self._pos = 0

	@property
	def bit_len(self):
		return self._bitlen

	def seek(self, pos: int):
		self._pos = pos

	def _convpos(self, pos: int):
		(bytepos, bitpos) = divmod(pos, 8)
		bitpos = 7 - bitpos
		return (bytepos, bitpos)

	def set_bit(self, pos: int, value: int):
		assert(value in [ 0, 1 ])
		(bytepos, bitpos) = self._convpos(pos)
		missing_chars = bytepos + 1 - len(self._bs)
		if missing_chars > 0:
			self._bs += bytes(missing_chars)
		if value == 0:
			self._bs[bytepos] &= ~(1 << bitpos)
		else:
			self._bs[bytepos] |= (1 << bitpos)
		self._bitlen = max(self._bitlen, pos + 1)

	def get_bit(self, pos: int):
		(bytepos, bitpos) = self._convpos(pos)
		if bytepos < len(self._bs):
			return (self._bs[bytepos] & (1 << bitpos)) != 0
		else:
			return False

	def append(self, bit: int):
		assert(bit in [ 0, 1 ])
		self.set_bit(self._bitlen, bit)

	def append_value(self, value: int, bitcount: int):
		for i in range(bitcount):
			if (1 << i) & value:
				self.append(1)
			else:
				self.append(0)

	def read_bits(self, count):
		result = 0
		for i in range(count):
			result |= self.get_bit(self._pos + i) << i
		self._pos += count
		return result

	def read_chars(self, count):
		result = bytearray(count)
		for i in range(count):
			result[i] = self.read_bits(8)
		return result

	@classmethod
	def _from_6bit_alphabet(cls, input_text, alphabet):
		assert(len(alphabet) == 64)
		bitstring = BitString()
		for char in input_text:
			if char not in alphabet:
				break
			else:
				bitstring.append_value(alphabet[char], 6)
		return bitstring

	def _to_6bit_alphabet(self, alphabet: str):
		assert(len(alphabet) == 64)
		char_count = (self.bit_len + 5) // 6
		result = [ ]
		self.seek(0)
		for charno in range(char_count):
			index = self.read_bits(6)
			result.append(alphabet[index])
		return "".join(result)

	@classmethod
	def from_base64(cls, input_text: str):
		return cls._from_6bit_alphabet(input_text, cls._BASE64)

	@classmethod
	def from_url_component(cls, input_text: str):
		return cls._from_6bit_alphabet(input_text, cls._URI_COMPONENT)

	@classmethod
	def from_bit_text(cls, text: str):
		bitstring = BitString()
		for char in text:
			if char == "0":
				bitstring.append(0)
			elif char == "1":
				bitstring.append(1)
		return bitstring

	@classmethod
	def from_bytes(cls, data: bytes):
		bitstring = BitString()
		bitstring._bs = bytearray(data)
		bitstring._bitlen = len(data) * 8
		return bitstring

	def to_base64(self):
		return self._to_6bit_alphabet(self._INV_BASE64)

	def to_url_component(self):
		return self._to_6bit_alphabet(self._INV_URI_COMPONENT)

	def to_text(self):
		return "".join("1" if self.get_bit(i) else "0" for i in range(self._bitlen))

	def __bytes__(self):
		return bytes(self._bs)

	def __eq__(self, other):
		return (self._bitlen == other._bitlen) and (self._bs == other._bs)

	def __repr__(self):
		return f"BitString<{self._bitlen} bits: {self.to_text()}>"
