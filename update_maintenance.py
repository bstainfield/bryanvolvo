import sys, csv, getopt, codecs, datetime
from collections import OrderedDict

class Maintenance(object):
   def __init__(self):
      self.total_distance = 0
      self.average_mileage_day = 0
      self.next_date_service = datetime.date.today()
      self.car_epoch = datetime.date(2016, 7, 8)
      self.milestone = 0
      self.days_until_service = 0

def get_distance(entry):
   return float(entry.split(';')[2])

def get_date(entry):
   date_str = entry.split(';')[1]
   date = datetime.datetime.strptime(date_str, "%m/%d/%y").date()
   return date

def parse_csv(inputfile):
   reader = csv.reader(codecs.open(inputfile,'rU','utf-16'))
   maintenance = Maintenance()
   total_distance = 0
   latest_day = maintenance.car_epoch
   for line in reader:
      distance = 0
      if len(line) == 1:
         continue
      try:
         distance = get_distance(line[4])
      except:
         pass
      maintenance.total_distance += distance
      date = get_date(line[0])
      if date > latest_day: latest_day = date
   maintenance.average_mileage_day = maintenance.total_distance / (latest_day - maintenance.car_epoch).days
   if 0 <= maintenance.total_distance <= 10000:
      days_remaining = (10000 - maintenance.total_distance) / maintenance.average_mileage_day
      maintenance.milestone = 10000
   elif 10000 < maintenance.total_distance <= 20000:
      days_remaining = (20000 - maintenance.total_distance) / maintenance.average_mileage_day
      maintenance.milestone = 20000
   elif 20000 < maintenance.total_distance:
      days_remaining = (30000 - maintenance.total_distance) / maintenance.average_mileage_day
      maintenance.milestone = 30000
   else:
      days_remaining = -1
   maintenance.days_until_service = int(days_remaining)
   maintenance.next_date_service = latest_day + datetime.timedelta(days=days_remaining)
   return maintenance

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
   maintenance = parse_csv(inputfile)
   print "Distance,Milestone,Date,Days"
   print "{0},{1},{2},{3}".format(maintenance.total_distance,
                                  maintenance.milestone,
                                  maintenance.next_date_service,
                                  maintenance.days_until_service)

if __name__ == "__main__":
   main(sys.argv[1:])