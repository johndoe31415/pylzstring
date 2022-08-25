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

import unittest
from lzstr import BitString

class BitStringTests(unittest.TestCase):
	def test_bitstring_bitorder(self):
		bs = BitString()
		bs.append_value(12345, 17)
		bs.append_value(54321, 19)
		bs.seek(0)
		self.assertEqual(bs.read_bits(17), 12345)
		self.assertEqual(bs.read_bits(19), 54321)

	def test_bitstring_bittext(self):
		text = "001000001000001000010000110000100100000000"
		bs = BitString.from_bit_text(text)
		for (bitno, value) in enumerate(text):
			self.assertEqual(bs.get_bit(bitno), int(value))
