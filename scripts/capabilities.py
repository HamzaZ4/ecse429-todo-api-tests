"""Prints every request in the Postman collection as a curl command (the 'capabilities' list).

Usage: python scripts/capabilities.py ECSE429.postman_collection.json
"""
import json
import sys


def walk(items):
    for item in items:
        if "item" in item:
            yield from walk(item["item"])
        else:
            yield item


def main(path):
    with open(path) as handle:
        collection = json.load(handle)
    for item in walk(collection["item"]):
        request = item["request"]
        headers = " ".join(f"-H '{h['key']}: {h['value']}'" for h in request.get("header", []))
        body = request.get("body", {}).get("raw")
        data = f" -d '{body}'" if body else ""
        url = request["url"]["raw"].replace("{{baseUrl}}", "http://localhost:4567")
        print(f"# {item['name']}\ncurl -i -X {request['method']} {headers}{data} '{url}'\n")


if __name__ == "__main__":
    main(sys.argv[1])
