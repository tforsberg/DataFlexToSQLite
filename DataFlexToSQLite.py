from core import Converter

if __name__ == "__main__":
	converter = Converter.Converter("/home/joaoluiz/solisoft/Projetos/TMP/DATAFLEX/MAQUINAS/MAQUINAS.DAT")
	print "DBName: %s" % converter.get_db_name()
	print "NumRecords: %d" % converter.get_total_records()
	#print "Record Length: %d" % converter.get_record_length()
	print "Total Columns: %d" % converter.get_total_columns()
	converter.teste()
	
	