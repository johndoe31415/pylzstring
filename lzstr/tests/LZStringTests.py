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

import os
import unittest
import pkgutil
import json
from lzstr import BitString, LZStringDecompressor, LZStringCompressor

class LZStringTests(unittest.TestCase):
	def setUp(self):
		self._test_vectors = json.loads(pkgutil.get_data("lzstr.tests", "test_vectors.json"))
		for test_vector in self._test_vectors:
			test_vector["uncompressed"] = test_vector["uncompressed"].encode("ascii")

	def test_decompress_abc(self):
		bs = BitString.from_bit_text("001000001000001000010000110000100100")
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

	def test_run_vectors_base64_decompression(self):
		for test_vector in self._test_vectors:
			bs = BitString.from_base64(test_vector["base64"])
			self.assertEqual(LZStringDecompressor(bs).decompress(), test_vector["uncompressed"])

	def test_run_vectors_url_component_decompression(self):
		for test_vector in self._test_vectors:
			bs = BitString.from_url_component(test_vector["uri"])
			self.assertEqual(LZStringDecompressor(bs).decompress(), test_vector["uncompressed"])

	def test_run_vectors_binary_decompression(self):
		for test_vector in self._test_vectors:
			bs = BitString.from_bytes(bytes(test_vector["uint8"]))
			self.assertEqual(LZStringDecompressor(bs).decompress(), test_vector["uncompressed"])

	def test_run_vectors_compression(self):
		for test_vector in self._test_vectors:
			reference_bs = BitString.from_bytes(bytes(test_vector["uint8"]))
			compressed = LZStringCompressor(test_vector["uncompressed"]).compress()
			if compressed.bit_len < reference_bs.bit_len:
				# Pad with zeros
				pad_bits = reference_bs.bit_len - compressed.bit_len
				compressed.append_value(0, pad_bits)
			self.assertEqual(reference_bs, compressed)

	def test_run_vectors_decompressible(self):
		# Check that every word can be successfully decompressed, not
		# necessarily outputs the same compressed stream
		for test_vector in self._test_vectors:
			uncompressed = test_vector["uncompressed"]
			compressed = LZStringCompressor(uncompressed).compress()
			decompressed = LZStringDecompressor(compressed).decompress()
			self.assertEqual(decompressed, uncompressed)

	def test_convenience_bytes(self):
		random_data = os.urandom(1000)
		compressed = LZStringCompressor.compress_to_bytes(random_data)
		self.assertTrue(isinstance(compressed, bytes))
		decompressed = LZStringDecompressor.decompress_from_bytes(compressed)
		self.assertEqual(random_data, decompressed)

	def test_convenience_base64(self):
		random_data = os.urandom(1000)
		compressed = LZStringCompressor.compress_to_base64(random_data)
		self.assertTrue(isinstance(compressed, str))
		decompressed = LZStringDecompressor.decompress_from_base64(compressed)
		self.assertEqual(random_data, decompressed)

	def test_convenience_url_component(self):
		random_data = os.urandom(1000)
		compressed = LZStringCompressor.compress_to_url_component(random_data)
		self.assertTrue(isinstance(compressed, str))
		decompressed = LZStringDecompressor.decompress_from_url_component(compressed)
		self.assertEqual(random_data, decompressed)
