import requests
import json
from datetime import datetime  
from datetime import timedelta  

class Patient:
	avg = 0

	def __init__(self, date):  
		self.start = date

	def endToday(self,date):
		self.end = date
		self.avg = self.end-self.start

def avg_rec_time_kerala():

	response = requests.get("https://keralastats.coronasafe.live/histories.json")

	data = json.loads(response.content)

	patients = []

	lastRecovered = 0;

	days = data['histories']
	dist_count = {"Alappuzha":0,"Ernakulam":0,"Idukki":0,"Kannur":0,"Kasaragod":0,"Kollam":0,"Kottayam":0,"Kozhikode":0,"Malappuram":0,"Palakkad":0,"Pathanamthitta":0,"Thiruvananthapuram":0,"Thrissur":0,"Wayanad":0}
	dist_recov = {"Alappuzha":0,"Ernakulam":0,"Idukki":0,"Kannur":0,"Kasaragod":0,"Kollam":0,"Kottayam":0,"Kozhikode":0,"Malappuram":0,"Palakkad":0,"Pathanamthitta":0,"Thiruvananthapuram":0,"Thrissur":0,"Wayanad":0}

	daily_patients  = [0]*len(days)

	for i in range(len(days)):
		dayDelta = days[i]['summary']
		for d in dayDelta:
			dist = dayDelta[d]

			
			# Update New Cases

			new_cases = int(dist["confirmed"]) - dist_count[d]
			for x in range(new_cases):
				patients.append(Patient(i))
			dist_count[d] = int(dist["confirmed"])
			daily_patients[i] += new_cases

			# Update Recovered

			new_recovs = int(dist["recovered"]) - dist_recov[d]
			for x in range(new_recovs):
				patients[lastRecovered].endToday(i)
				lastRecovered = lastRecovered+1

			dist_recov[d] = int(dist["recovered"])



	print("Total Patients : "+str(len(patients)))
	print("Total Recovered : "+str(lastRecovered))


	avg = 0
	for p in patients:
		avg += p.avg

	avg = int(avg/lastRecovered)

	print("Avg Recovery Time : "+str(avg) + " Days")

	print("\n\n")

	print("Recovery Prediction for Next days")

	nextRecovery = daily_patients[-avg:]
	today = datetime.now()

	for i in range(len(nextRecovery)):
		thisDay = today + timedelta(days=i+1)
		print(thisDay.strftime("%B %d") + " :\t" + str(nextRecovery[i]))


def avg_rec_time_india():

	response = requests.get("https://api.covid19india.org/data.json")

	data = json.loads(response.content)

	patients = []

	lastRecovered = 0;

	days = data['cases_time_series']
	for i in range(len(days)):
		day = days[i]


		for x in range(int(day["dailyconfirmed"])):
			patients.append(Patient(i))

		# Update Recovered
		for x in range(int(day["dailyrecovered"])):
			patients[lastRecovered].endToday(i)
			lastRecovered = lastRecovered+1


	print("Total Patients : "+str(len(patients)))
	print("Total Recovered : "+str(lastRecovered))


	avg = 0
	for p in patients:
		avg += p.avg

	avg = avg/lastRecovered

	print("Avg Recovery Time : "+str(int(avg)) + " Days")





if __name__ == "__main__":	
	print()
	print("Kerala Status\n===================")
	avg_rec_time_kerala()
	
	print()
	print("India Status\n===================")
	avg_rec_time_india()