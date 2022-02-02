import pandas as pd
import geopandas
import sys, os
#Counties
string = " Carlow, Cavan, Clare, Cork, Donegal, Dublin, Galway, Kerry, Kildare, Kilkenny, Laois, Leitrim, Limerick, Longford, Louth, Mayo, Meath, Monaghan, Offaly, Roscommon, Sligo, Tipperary, Waterford, Westmeath, Wexford, Wicklow"
string = string.upper()
counties=list(string.split(','))
for element in range(len(counties)):
        counties[element] = counties[element].strip(' ')
# print(counties)
addresses = {}


#Read the csv file

add = pd.read_csv('addresses_for_task.csv', float_precision=None)
# print(add.head(1))
# add = add.head(5)

townlands = geopandas.read_file('Townlands_-_OSi_National_Placenames_Gazetteer.geojson')
townlands=townlands[['County', 'Local_Government_Area', 'English_Name', 'geometry']]


#Function to handle Address
def get_address(address):
    try:
        #Extract based on comma
        # print("Extract townland and county")
        split_add = list((address.split(',')))
        for element in range(len(split_add)):
            split_add[element] = split_add[element].strip(' ')
        county= split_add[-1]
        townloand = split_add[-3]
        # print("Townland {}, County {}".format(townloand, county))
        coordinates = get_coor_townland(townloand, county)
        return coordinates
    except:
        try:
            # print("Extracting only county from the address")
            split_add = list((address.split(' ')))
            for element in range(len(split_add)):
                split_add[element] = split_add[element].strip(' ')
            county= split_add[-1]
            # print("County {}".format(county))
            coordinates = get_coor_county(county)
            return coordinates
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

#Function to get coordinates
def get_coor_townland(townloand, county):
    # print("Inside get_coor_townland")
    try:
        # filter dataframe
        geometry = str(townlands.loc[(townlands['County']==county) & (townlands['English_Name']==townloand),
                            ['geometry']].iloc[[0]]) 
        coordinates=list((geometry[geometry.find('(')+len('('):geometry.find(')')]).split(' '))
        # print("{} , {}".format(coordinates[0], coordinates[1]))
        return coordinates
    except:
        try:
            coordinates = get_coor_county(county)
            return coordinates
        except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
    
def get_coor_county(county):
    # print('Getting the coordinates of the county')
    
    for text in counties:
        if county in text:
            county= text
            break
    # print(county)
    try: 
        geometry = str(townlands.loc[(townlands['County']==county),['geometry']].iloc[[0]]) 
        # print(geometry)
        coordinates=list((geometry[geometry.find('(')+len('('):geometry.find(')')]).split(' '))
        # print("{} , {}".format(coordinates[0], coordinates[1]))
        return coordinates
    except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

try: 
    for ind in add.index:
        # print(add['Address'][ind])
        address=add['Address'][ind].upper()
        # address = ('Killagh, Doolin, clar').upper()
        coordinates = get_address(address)
        # get_address(address)
        # print(coordinates)
        # print(type(coordinates))
        # coordinate = str(coordinates[0])+" , "+str(coordinates[1])
        addresses[address] = coordinates
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)

#print the result
for key, value in addresses.items():
    print("{} : {}".format(key,value))
    
print(len(addresses))