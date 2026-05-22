# import necessary modules
import json
import unittest
import datetime

# open and read json files using UTF-8 encoding
with open("./data-1.json", "r", encoding="utf-8") as f:
    jsonData1 = json.load(f)

with open("./data-2.json", "r", encoding="utf-8") as f:
    jsonData2 = json.load(f)

with open("./data-result.json", "r", encoding="utf-8") as f:
    jsonExpectedResult = json.load(f)


# convert json data from format 1 to the expected unified format
def convertFromFormat1(jsonObject):

    # split location string
    locationParts = jsonObject["location"].split("/")

    # create unified output
    result = {
        "deviceID": jsonObject["deviceID"],
        "deviceType": jsonObject["deviceType"],
        "timestamp": jsonObject["timestamp"],
        "location": {
            "country": locationParts[0],
            "city": locationParts[1],
            "area": locationParts[2],
            "factory": locationParts[3],
            "section": locationParts[4]
        },
        "data": {
            "status": jsonObject["operationStatus"],
            "temperature": jsonObject["temp"]
        }
    }

    return result


# convert json data from format 2 to the expected unified format
def convertFromFormat2(jsonObject):

    # convert ISO timestamp to milliseconds since epoch
    data = datetime.datetime.strptime(
        jsonObject["timestamp"],
        "%Y-%m-%dT%H:%M:%S.%fZ"
    )

    timestamp = round(
        (data - datetime.datetime(1970, 1, 1)).total_seconds() * 1000
    )

    # create unified output
    result = {
        "deviceID": jsonObject["device"]["id"],
        "deviceType": jsonObject["device"]["type"],
        "timestamp": timestamp,
        "location": {
            "country": jsonObject["country"],
            "city": jsonObject["city"],
            "area": jsonObject["area"],
            "factory": jsonObject["factory"],
            "section": jsonObject["section"]
        },
        "data": jsonObject["data"]
    }

    return result


# main function
def main(jsonObject):

    result = {}

    # check which format is being used
    if jsonObject.get("device") is None:
        result = convertFromFormat1(jsonObject)
    else:
        result = convertFromFormat2(jsonObject)

    return result


# unit tests
class TestSolution(unittest.TestCase):

    # sanity test
    def test_sanity(self):

        result = json.loads(json.dumps(jsonExpectedResult))

        self.assertEqual(
            result,
            jsonExpectedResult
        )

    # test conversion from format 1
    def test_dataType1(self):

        result = main(jsonData1)

        self.assertEqual(
            result,
            jsonExpectedResult,
            "Converting from Type 1 failed"
        )

    # test conversion from format 2
    def test_dataType2(self):

        result = main(jsonData2)

        self.assertEqual(
            result,
            jsonExpectedResult,
            "Converting from Type 2 failed"
        )


# run tests
if __name__ == "__main__":
    unittest.main()