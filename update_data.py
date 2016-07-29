import sys, csv, getopt, codecs, datetime
from collections import OrderedDict

first_day = datetime.date(2016, 7, 8)
per_diem = 10000/365

class Day(object):

   def __init__(self, date, distance, fuel):
      self.date = date
      self.distance = distance
      self.fuel = fuel
      self.allotment = (date - first_day).days * per_diem
      try:
         self.mpg = distance/fuel
      except:
         self.mpg = 0
      self.age = (date - first_day).days

   def displayDay(self):
      self.mpg = self.distance/self.fuel
      print " Distance: ", self.distance, " Fuel: ", self.fuel,\
      " MPG: ", self.mpg, " Allotment: ", self.allotment,\
      " Days owned: ", self.age

   def csv_day(self):
      self.mpg = self.distance/self.fuel
      #"date; distance; fuel; mpg; "
      return [self.date, self.distance, self.fuel, self.mpg, self.allotment]

def get_date(entry):
   date_str = entry.split(';')[1]
   date = datetime.datetime.strptime(date_str, "%m/%d/%y").date()
   return date

def get_fuel(entry):
   return float(entry.split(';')[3])

def get_distance(entry):
   return float(entry.split(';')[2])

def parse_csv(inputfile):
   reader = csv.reader(codecs.open(inputfile,'rU','utf-16'))
   journal = {}
   for line in reader:
      if len(line) == 1:
         continue
      date = get_date(line[0])
      fuel = get_fuel(line[4])
      distance = get_distance(line[4])
      if date in journal:
         journal[date].distance += distance
         journal[date].fuel += fuel
      else:
         journal[date] = Day(date, distance, fuel)

   return journal

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
   if verbose:
      for date, entry in output.items():
         print date, ": ", entry.displayDay()
   else:
      i = 1
      total_distance = 0
      print "date;distance;fuel;mpg;total distance;total allotment"
      for date, entry in OrderedDict(sorted(output.items(), key=lambda t: t[0])).items():
         csv_day = entry.csv_day()
         if csv_day != None: #idk why
            total_distance += entry.distance
            for value in csv_day:
               print value, ";",
            print total_distance, ";"
            i += 1

if __name__ == "__main__":
   main(sys.argv[1:])