from dataclasses import dataclass
from enum import Enum
import json
import time
import requests
from typing import Dict
import os
import pandas as pd

SLEEP_TIME = 1


class AreaType(Enum):
    CITY = 1
    DISTRICT = 2
    NEIGHBORHOOD = 3
    SCHOOL = 4
    SANDIK = 5

@dataclass
class School:
    id: int
    name: str
    neighborhood_id: int

    def __init__(self, id, name, city_id, district_id, neighborhood_id):
        self.id = id
        self.name = name
        self.city_id = city_id
        self.district_id = district_id
        self.neighborhood_id = neighborhood_id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "city_id": self.city_id,
            "district_id": self.district_id,
            "neighborhood_id": self.neighborhood_id
        }
    
    def __str__(self):
        return f"{self.id} - {self.name} - {self.city_id} - {self.district_id} - {self.neighborhood_id}"

@dataclass
class Neighborhood:
    id: int
    name: str
    city_id: int
    district_id: int
    schools: list[School]

    def __init__(self, id, name, city_id, district_id):
        self.id = id
        self.name = name
        self.city_id = city_id
        self.district_id = district_id
        self.schools = []
        schools = send_request(AreaType.SCHOOL, city_id=self.city_id, district_id=self.district_id, neighborhood_id=self.id)
        for school in schools:
            self.schools.append(School(id=school["id"], name=school["name"], city_id=self.city_id, district_id=self.district_id, neighborhood_id=self.id))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "city_id": self.city_id,
            "district_id": self.district_id,
            "schools": [school.to_dict() for school in self.schools]
        }
    
    def __str__(self):
        return f"{self.id} - {self.name}"


@dataclass
class District:
    id: int
    name: str
    city_id: int
    neighborhoods: list[Neighborhood]

    def __init__(self, id, name, city_id):
        self.id = id
        self.name = name
        self.city_id = city_id
        self.neighborhoods = []
        neighborhoods = send_request(AreaType.NEIGHBORHOOD, city_id=self.city_id, district_id=self.id)
        for neighborhood in neighborhoods:
            self.neighborhoods.append(Neighborhood(id=neighborhood["id"], name=neighborhood["name"], city_id=self.city_id, district_id=self.id))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "city_id": self.city_id,
            "neighborhoods": [neighborhood.to_dict() for neighborhood in self.neighborhoods]
        }
    
    def __str__(self):
        return f"{self.id} - {self.name} - {self.neighborhoods.count()}"


@dataclass
class City:
    id: int
    name: str
    plate: int
    districts: list[District]

    def __init__(self, id, name, plate):
        self.id = id
        self.name = name
        self.plate = plate
        self.districts = []
        districts = send_request(AreaType.DISTRICT, city_id=self.id)
        for district in districts:
            self.districts.append(District(id=district["id"], name=district["name"], city_id=self.id))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "plate": self.plate,
            "districts": [district.to_dict() for district in self.districts]
        }

    def __str__(self):
        return f"{self.id} - {self.name} - {self.plate} - {self.districts.count()}"

@dataclass
class CMResultClass:
    image_url: str
    submission_id: int
    total_vote: int
    votes: Dict[str, int]


@dataclass
class ResultElement:
    ballot_box_number: int
    cm_result: CMResultClass
    mv_result: CMResultClass
    school_name: str


def send_request(type, city_id=0, district_id=0, neighborhood_id=0, school_id=0):
    CITIES_URL = f"https://api-sonuc.oyveotesi.org/api/v1/cities"
    DISTRICTS_URL = f"https://api-sonuc.oyveotesi.org/api/v1/cities/{city_id}/districts"
    NEIGHBORHOODS_URL = f"https://api-sonuc.oyveotesi.org/api/v1/cities/{city_id}/districts/{district_id}/neighborhoods"
    SCHOOLS_URL = f"https://api-sonuc.oyveotesi.org/api/v1/cities/{city_id}/districts/{district_id}/neighborhoods/{neighborhood_id}/schools"

    if type == AreaType.CITY:
        url = CITIES_URL
    elif type == AreaType.DISTRICT:
        url = DISTRICTS_URL
    elif type == AreaType.NEIGHBORHOOD:
        url = NEIGHBORHOODS_URL
    elif type == AreaType.SCHOOL:
        url = SCHOOLS_URL
    else:
        print("Error: type is not valid")
        exit(1)

    try:
        time.sleep(SLEEP_TIME)
        print(f"Sending request to {url}")
        response = requests.get(
            url=url,
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        return response.json()
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
        return []


def gather_all():
    cities = get_cities()
    print_cities(cities)
    print("Gathered all cities")

def print_cities(cities):
    cities_dict = [city.to_dict() for city in cities]

    with open("tree.json", "w", encoding="utf-8") as f:
        json.dump(cities_dict, f, ensure_ascii=False, indent=4)


def get_cities():
    with open("cities.json", "r", encoding="utf-8") as f:
        cities_json = json.load(f)

    cities = [City(id=city["id"], name=city["name"], plate=city["plate"]) for city in cities_json]

    return cities


def send_request_sandik(school_id):
    SANDIKS_URL = f"https://api-sonuc.oyveotesi.org/api/v1/submission/school/{school_id}"

    try:
        time.sleep(SLEEP_TIME)
        print(f"Sending request to {SANDIKS_URL}")
        response = requests.get(
            url=SANDIKS_URL,
			headers={
				"User-Agent":"Mozilla/5.0"
			}
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        return response.json()
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
        return []
    
if __name__ == "__main__":
    with open("cities.json", "r", encoding="utf-8") as f:
        cities_json = json.load(f)
    
    city_plate = int(input("Enter city plate: "))

    city = None
    for city_json in cities_json:
        if city_json["plate"] == city_plate:
            city = City(id=city_json["id"], name=city_json["name"], plate=city_json["plate"])
            break

    if city is None:
        print("Error: city not found")
        exit(1)

    filename = f"{city.name}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(city.to_dict(), f, ensure_ascii=False, indent=4)
    print(f"Wrote to {filename}")

    print(f"Gathered city {city.name}")

    # real data coming

    city_name=city.name
    city_file_name = filename
    #city_name="BAYBURT"
    #city_file_name="BAYBURT.json"
    with open(city_file_name, 'r', encoding="utf-8") as f:
        city = json.load(f)
    city_folder = f'{city_name}' 
    if not os.path.exists(city_folder):
        os.makedirs(city_folder)
    for district in city["districts"]:
        for neighborhood in district["neighborhoods"]:
            for school in neighborhood["schools"]:
                school_id = school["id"]
                results = send_request_sandik(school_id)

                filename = f"{city_folder}/school_{school_id}.json"
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(results, f, ensure_ascii=False, indent=4)
                try:
                    pd.DataFrame([result["cm_result"] for result in results]).to_excel(f"{city_folder}/school_{school_id}_cm_results.xlsx")
                    pd.DataFrame([result["mv_result"] for result in results]).to_excel(f"{city_folder}/school_{school_id}_mv_results.xlsx")
                except:
                    pass
                if len(results) > 0:
                    for result in results:
                        ballot_folder = f"{city_folder}/{result['school_name']}"
                        if not os.path.exists(ballot_folder):
                            os.makedirs(ballot_folder)
                        try:
                            pd.DataFrame([result["cm_result"]]).to_excel(f"{ballot_folder}/cm_results_{result['ballot_box_number']}.xlsx")
                            pd.DataFrame([result["mv_result"]]).to_excel(f"{ballot_folder}/mv_results_{result['ballot_box_number']}.xlsx")
                        except:
                            pass
                        try:
                            time.sleep(SLEEP_TIME*2)
                            response = requests.get(
                                url=result["cm_result"]["image_url"],
                                headers={
                                    "User-Agent":"Mozilla/5.0"
                                }
                            )
                            with open(f"{ballot_folder}/cm_result__{result['ballot_box_number']}.jpg", "wb") as f:
                                f.write(response.content)
                        except Exception as e:
                            print("failed to get cm_result image",e)
                        try:
                            time.sleep(SLEEP_TIME*2)
                            response = requests.get(
                                url=result["mv_result"]["image_url"],
                                headers={
                                    "User-Agent":"Mozilla/5.0"
                                }
                            )
                            with open(f"{ballot_folder}/mv_result__{result['ballot_box_number']}.jpg", "wb") as f:
                                f.write(response.content)
                        except Exception as e:
                            print("failed to get mv_result image",e)
                print()
                


