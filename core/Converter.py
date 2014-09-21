import struct
import binascii
from core import Field

class Converter:
	def __init__(self, dat_file):
		self.dat_file = dat_file
		self.read_dat()


	def read_dat(self):
		fp = open(self.dat_file, "rb")
		try:
			self.data = fp.read()
		finally:
			fp.close()

	def get_range_byte(self, ini, end):
		return self.data[ini:end];

	def byte_to_string(self, bytes_s):
		return bytes_s.decode("utf-8").strip()


	def byte_to_int(self, bytes_s):
		return struct.unpack('I', bytes_s)[0]
	
	def byte_to_short_int(self, bytes_s):
		return struct.unpack('H', bytes_s)[0]
	
	def byte_to_char(self, bytes_s):
		return struct.unpack('B', bytes_s)[0]
		

	def get_db_name(self):
		return self.byte_to_string(self.get_range_byte(0x2d0,0x2d0+16))
	
	def get_total_records(self):
		return self.byte_to_int(self.get_range_byte(0x0,0x0+4))

	def get_record_length(self):
		return self.byte_to_short_int(self.get_range_byte(0x9a, 0x9a+2))

	def get_total_columns(self):
		return self.byte_to_short_int(self.get_range_byte(0xa5, 0xa5+2))

	def byte_to_hex(self, bytes_s):
		return binascii.hexlify(bytes_s)

	def get_columns(self):
		tmp_offset = 0
		tmp_size = 3
		tmp_type = 4
		self.columns = []
		for x in range(self.get_total_columns()):
			field = Field.Field()
			offset = x * 8; 
			field.offset = self.byte_to_short_int(self.get_range_byte(0x2e0+offset, 0x2e0 + offset +2))
			field.size = self.byte_to_char(self.get_range_byte(0x2e0+offset + tmp_size, 0x2e0 + offset + tmp_size + 1))
			field.type = self.byte_to_char(self.get_range_byte(0x2e0+offset + tmp_type, 0x2e0 + offset + tmp_type + 1))
			field.name = 'Column %d' % x
			self.columns.append(field)
		return self.columns

	def teste2(self):
		start = 0
		offset = 8 * self.get_total_columns()
		while start < offset:
			start += 512
		start += self.get_record_length()	
		for field in self.get_columns():
			offset = field.offset -1
			size = field.size
			tp = field.type
			if tp == 0: # String
				print self.byte_to_char(self.get_range_byte(0x0c00+start,0x0c00 +start +self.get_record_length()))
	def teste(self):
		
		total_records = self.get_total_records()
		str_buffer = ""
		start = 0
		offset = self.get_total_columns()
		while start < offset:
			start += 512
		start += self.get_record_length()

		"""
		for row in range(total_records-400):
			column = 0
			for field in self.get_columns():
				offset = field.offset
				column += 1
				size = field.size
				tp = field.type
				if tp == 0: #String
					for x in range(size-1):
						tmp = (0x0c00 + start + row + column + x) * 16
						str_buffer += chr(self.byte_to_char(self.get_range_byte(tmp,tmp+1)))
				
			"""
		
		for row in range(self.get_total_records()-439):
			column = 0
			colunas = ""
			tmp = ""
			for field in self.get_columns():
					offset = field.offset -1
					column += 1
					size = field.size
					tp = field.type
					
					offset = 0x0c00 + start + offset + (row * 512)
					if tp == 0: #String
						#offset = 0x0c00 + start + column + (row * 8) 
						#print "OFFSET: %d" % offset
						#print "size: %d" % size
						str_buffer = ""
						row_bytes = self.get_range_byte(offset, offset + size)
						for byte in row_bytes:
							str_buffer += chr(self.byte_to_char(byte))
						colunas += "%2d: %s\t\t" % (column, str_buffer)
					if tp == 1 or tp == 3:
						num = -1
						if size == 2:
							num = self.byte_to_short_int(self.get_range_byte(offset+1, offset + 3))
							#num = self.byte_to_hex(self.get_range_byte(offset+1, offset + size))
						if size == 4:
							num = self.byte_to_int(self.get_range_byte(offset+1, offset + 5))
							#num = self.byte_to_hex(self.get_range_byte(offset+1, offset + size))
						colunas += "%2d: %s\t\t" % (column, num)
			print colunas









