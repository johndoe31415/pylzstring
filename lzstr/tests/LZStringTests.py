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
from lzstr import BitString, LZStringDecompressor

class LZStringTests(unittest.TestCase):
	def test_decompress_abc(self):
		bs = BitString.from_bit_text("001000001000001000010000110000100100000000")
		self.assertEqual(LZStringDecompressor(bs).decompress(), b"ABC")

	def test_decompress_abc_base64(self):
		bs = BitString.from_base64("IIIQwkA=")
		self.assertEqual(LZStringDecompressor(bs).decompress(), b"ABC")

	def test_decompress_aaa_url_component(self):
		bs = BitString.from_url_component("IY1-kA")
		self.assertEqual(LZStringDecompressor(bs).decompress(), b"aaaaaaaaaaaaaaaaaaaa")

	def test_decompress_aaa_base64(self):
		bs = BitString.from_base64("IY1/kA==")
		self.assertEqual(LZStringDecompressor(bs).decompress(), b"aaaaaaaaaaaaaaaaaaaa")

	def test_decompress_circuitjs(self):
		bs = BitString.from_url_component("CQAgjCAMB0l3BWc0FwCwCY0HYEA4cEMElURTJyBTAWjDACgwE0QMs21KBmANj06VKGKOSZl2rMGlZ8B01sNEIGAGXAZ5vSnkphtbUQDMAhgBsAzlXJQ1GgZJC62HEZVOXrSSAwDu9lykDRx9-fWEOcIDQ8AMwTUDov1iI1kcQ5PitPQBOESiYsDyU8GLiXlswsoQK9JrK0vzgyIMfAFkQOXAZEDR9brS2FAYOrqxKPtquQwxhoA")
		self.assertEqual(LZStringDecompressor(bs).decompress(), b"$ 1 0.000005 1.500424758475255 50 5 50 5e-11\n154 224 240 368 240 0 2 0 5\n150 224 144 368 144 0 2 0 5\nL 128 160 80 160 2 0 false 5 0\nL 128 224 80 224 2 0 false 5 0\nw 128 224 160 224 0\nw 160 224 160 128 0\nw 160 128 224 128 0\nw 160 224 224 224 0\nw 128 160 192 160 0\nw 192 160 192 256 0\nw 192 256 224 256 0\nw 192 160 224 160 0\nM 368 144 416 144 2 2.5\nM 368 240 416 240 2 2.5\n")
