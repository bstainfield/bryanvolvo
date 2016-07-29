import sys, csv, getopt, codecs, datetime
from collections import OrderedDict

def get_distance(entry):
   return float(entry.split(';')[2])

def get_tag(entry):
   return entry.split(';')[0]

def parse_csv(inputfile):
   distances = {
      'Business': 0,
      'Private': 0,
      'Unassigned': 0
   }
   reader = csv.reader(codecs.open(inputfile,'rU','utf-16'))
   journal = {}
   for line in reader:
      if len(line) == 1:
         continue
      distances[get_tag(line[0])] += get_distance(line[4])
   return distances

def main(argv):
   inputfile = ''
   outputfile = ''
   verbose = False
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'tripcsv.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'tripcsv.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   output = parse_csv(inputfile)
   print "Business,Private,Unassigned"
   print "{0},{1},{2}".format(output['Business'],output['Private'],output['Unassigned'])

if __name__ == "__main__":
   main(sys.argv[1:])