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
	def test_bitstring_seek_retrieve(self):
		bs = BitString()
		bs.append_value(12345, 17)
		bs.append_value(54321, 19)
		bs.seek(0)
		self.assertEqual(bs.read_bits(17), 12345)
		self.assertEqual(bs.read_bits(19), 54321)

	def test_base64_representation(self):
		# "foobar"
		bs = BitString.from_base64("GYexCMEMCcg=")
		self.assertEqual(bytes(bs), bytes([ 25, 135, 177, 8, 193, 12, 9, 200, 0 ]))

		bs.seek(0)
		self.assertEqual(bs.read_bits(2), 0)
		self.assertEqual(bs.read_bits(8), ord("f"))
		self.assertEqual(bs.read_bits(3), 0)
		self.assertEqual(bs.read_bits(8), ord("o"))
		self.assertEqual(bs.read_bits(3), 4)
		self.assertEqual(bs.read_bits(3), 0)
		self.assertEqual(bs.read_bits(8), ord("b"))
		self.assertEqual(bs.read_bits(4), 0)
		self.assertEqual(bs.read_bits(8), ord("a"))
		self.assertEqual(bs.read_bits(4), 0)
		self.assertEqual(bs.read_bits(8), ord("r"))
		self.assertEqual(bs.read_bits(4), 2)

	def test_uint8_bit_order(self):
		# "ABCD"
		bs = BitString.from_bytes(bytes.fromhex("208210c202240000"))
		bs.seek(0)
		self.assertEqual(bs.read_bits(2), 0)
		self.assertEqual(bs.read_bits(8), ord("A"))
		self.assertEqual(bs.read_bits(3), 0)
		self.assertEqual(bs.read_bits(8), ord("B"))
		self.assertEqual(bs.read_bits(3), 0)
		self.assertEqual(bs.read_bits(8), ord("C"))
		self.assertEqual(bs.read_bits(4), 0)
		self.assertEqual(bs.read_bits(8), ord("D"))
		self.assertEqual(bs.read_bits(4), 2)
