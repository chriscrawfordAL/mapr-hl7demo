import random

#print(random.randint(0, 5))

otherHospitals = ['MidWsUnvMC','LakeMichMC','MidTwnUrgentC','SthrnMdwstMedCntr']

rand = random.randint(0, 3)
location = otherHospitals[rand]
print(location)
