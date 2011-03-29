import codecs

f = codecs.open('cities1000.txt', encoding='utf-8')
out = codecs.open( "capitals.csv", "w", "utf-8" )


out.write(u"%s;%s;%s;%s;%s;\n" % ("Name","Alt_name","lat", "lng", "Country_code") )
for line in f:
  data = line.split("\t")
  if data[7] == "PPLC":
    out.write(u"%s;%s;%s;%s;%s;\n" % (data[1],data[2],data[4], data[5], data[8]) )
    
out.close()