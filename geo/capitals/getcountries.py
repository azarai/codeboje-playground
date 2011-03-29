import codecs

f = codecs.open('countryInfoCSV.csv', encoding='utf-8')
capitals_in = codecs.open('capitals.csv', encoding='utf-8')
out = codecs.open( "countries_capitals.csv", "w", "utf-8" )

capitals = {}

for line in capitals_in:
  data = line.split(";")
  capitals[data[4]] = data

capitals_in.close()

out.write(u"%s;%s;%s;%s;%s;\n" % ("Country_Code","Country","Capital","Capital lat", " Capital lng") )
for line in f:
  if not line.startswith("iso"):
    data = line.split("\t")
    if capitals.has_key(data[0]):    
      capital = capitals[data[0]]
      out.write(u"%s;%s;%s;%s;%s;\n" % (data[0],data[4],capital[0],capital[2],capital[3]) )
    else:
      print "Capital missing for cc=%s, c=%s" % (data[0], data[5])
    
out.close()