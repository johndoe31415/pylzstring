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

from .BitString import BitString

class LZStringDecompressor():
	def __init__(self, bs: BitString):
		self._bs = bs
		self._numbits = 3
		self._enlargein = 4
		self._bs.seek(0)
		self._result = None

	def _enlarge_step(self):
		self._enlargein -= 1
		if self._enlargein == 0:
			self._enlargein = 1 << self._numbits
			self._numbits += 1

	def decompress(self):
		if self._result is not None:
			return self._result

		cdict = { i: bytearray([ i ]) for i in range(3) }
		match self._bs.read_bits(2):
			case 0:
				cdict[3] = self._bs.read_chars(1)
			case 1:
				cdict[3] = self._bs.read_chars(2)
			case _:
				return result

		self._result = cdict[3]
		last = cdict[3]
		while True:
			nextval = self._bs.read_bits(self._numbits)
			if nextval in [ 0, 1 ]:
				cdict[len(cdict)] = self._bs.read_chars(nextval + 1)
				nextval = len(cdict) - 1
				self._enlarge_step()
			elif nextval == 2:
				return self._result

			if nextval in cdict:
				entry = cdict[nextval]
			elif nextval == len(cdict):
				entry = last + bytearray([ last[0] ])
			else:
				raise LZDecompressionException(f"nextval {nextval} is not in cdict: {cdict}")

			self._result += entry

			cdict[len(cdict)] = last + bytearray([ entry[0] ])
			last = entry
			self._enlarge_step()
