from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as req
import csv
import os.path

import requests
import json
from datetime import datetime
import pytz
import folium
import matplotlib.pyplot as plt	

from pprint import pprint

air4thai_data = []
parser_file_name = 'air4thai.csv'

def Air4Thai_Data():
	url = 'http://air4thai.pcd.go.th/services/getNewAQI_JSON.php'
	read = requests.get(url)
	##print('read : ', read)
	temp_data = dict(read.json())
	##print('temp_data : ', temp_data)

	time_zone = pytz.timezone('Asia/Bangkok')	# Localize Time Zone
	##time_zone = pytz.timezone('US/Eastern')
	date_time = datetime.now(time_zone).strftime('%Y/%m/%d %H:%M:%S')
	print('time_zone : ', time_zone)	
	print('date_time : ', date_time)

	for i in temp_data['stations']:
		data_temp = {}
		last_temp = i['LastUpdate']

		data_temp['source'] = 'air4thai'
		data_temp['title_th'] = i['areaTH']			# Get area thai
		data_temp['title_en'] = i['areaEN']			# Get area english
		data_temp['time'] = last_temp['date'] + ' ' + last_temp['time']

		data_temp['Lat'] = i['lat']
		data_temp['Lng'] = i['long']
		data_temp['aqi'] = last_temp['AQI']['aqi']	# Get AQI data

		if 'PM25' in list(last_temp.keys()):		# Get PM2.5 data
			pm25 = last_temp['PM25']['value']
			if pm25 != 'n/a' and pm25 != '' and pm25 != '-' and pm25 != 'N/A':
				data_temp['pm2.5'] = pm25
			else:
				data_temp['pm2.5'] = ''
		else:
			data_temp['pm2.5'] = ''

		if 'PM10' in list(last_temp.keys()):		# Get PM10 data
			pm10 = last_temp['PM10']['value']
			if pm10 != 'n/a' and pm10 != '' and pm10 != '-' and pm10 != 'N/A':
				data_temp['pm10'] = pm10
			else:
				data_temp['pm10'] = ''
		else:
			data_temp['pm10'] = ''

		if 'CO' in list(last_temp.keys()):			# Get CO data
			co = last_temp['CO']['value']
			if co != 'n/a' and co != '' and co != '-' and co != 'N/A':
				data_temp['co'] = co
			else:
				data_temp['co'] = ''
		else:
			data_temp['co'] = ''

		if 'NO2' in list(last_temp.keys()):			# Get NO2 data
			no2 = last_temp['NO2']['value']
			if no2 != 'n/a' and no2 != '' and no2 != '-' and no2 != 'N/A':
				data_temp['no2'] = no2
			else:
				data_temp['no2'] = ''
		else:
			data_temp['no2'] = ''

		if 'O3' in list(last_temp.keys()):			# Get O3 data
			o3 = last_temp['O3']['value']
			if o3 != 'n/a' and o3 != '' and o3 != '-' and o3 != 'N/A':
				data_temp['o3'] = o3
			else:
				data_temp['o3'] = ''
		else:
			data_temp['o3'] = ''

		if 'SO2' in list(last_temp.keys()):			# Get SO2 data
			so2 = last_temp['SO2']['value']
			if so2 != 'n/a' and so2 != '' and so2 != '-' and so2 != 'N/A':
				data_temp['so2'] = o3
			else:
				data_temp['so2'] = ''
		else:
			data_temp['so2'] = ''

		air4thai_data.append(data_temp)

	print('===== Air4Thai Data =====')
	##print('Air4Thai Data : ', air4thai_data)
	##pprint(air4thai_data)
	for i in air4thai_data:
		print('Area : {} | PM2.5 : {}'.format(i['title_th'], i['pm2.5']))

def Write_Data():
	file_exists = os.path.isfile(parser_file_name)
	if file_exists:
		os.remove(parser_file_name)		# Remove existed file

	with open(parser_file_name,'a', newline="") as f:
		fw = csv.writer(f)
		row_list = []	# Clear row list

		for i in air4thai_data[0]:
			row_list.append(i)
		fw.writerow(row_list)

		for i in air4thai_data:
			row_list = []		# Clear row list for next row
			for j in i:
				row_list.append(i[j])
			fw.writerow(row_list)

def Map_Data():
	map_osm = folium.Map(location=[15.0000, 100.0000], zoom_start=5) 	# Center [latitude , longitude] and zoom lv.5
	tooltip = 'Click me!'	# Show tool tip
	for i in air4thai_data:
		if i['Lat'] == '' and i['Lng'] == '':
			continue	# Pass
		##print([(i['Lat'].strip()), (i['Lng'].strip())])
		folium.Marker([float(i['Lat'].strip()), float(i['Lng'].strip())], popup=i['pm2.5'] + ' µg/m³', tooltip=tooltip).add_to(map_osm)
	map_osm.save('air4thai.html') 	# Save to html

Air4Thai_Data()
Write_Data()
Map_Data()