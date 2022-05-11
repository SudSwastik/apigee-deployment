import asyncio
import aiohttp
import json
import sys
from collections import ChainMap
component_json = {
    "proxies": [],
    "sharedflows": [],
    "kvms": False,
    "targetServers": False,
    "apiProducts": False,
    "developers": False,
    "apps": False,
    "tests": False,
}
def parse_changed_components(data):
    print("data=")
    print(data)
    for path in data:
        component = path.split("/")
        print(component)
        if component[0] == "proxies":
            component_json["proxies"].append(component[1])
            component_json["tests"] = True
        if component[0] == "sharedflows":
            component_json["sharedflows"].append(component[1])
            component_json["tests"] = True
        if component[0] == "config":
            if component[-1] == "kvms.json":
                component_json["kvms"] = True
            if component[-1] == "targetServers.json":
                component_json["targetServers"] = True
            if component[-1] == "apiProducts.json":
                component_json["apiProducts"] = True
            if component[-1] == "developers.json":
                component_json["developers"] = True
            if component[-1] == "apps.json":
                component_json["apps"] = True
            if component[-1] == "caches.json":
                component_json["caches"] = True
    print("component_json=")
    print(component_json)
# def parse_health_check_urls(branch_name, urls):
#     health_check_urls = {}
#     for proxy in urls:
#         for changed_proxy in component_json["proxies"]:
#             if proxy == changed_proxy:
#                 if branch_name == "master":
#                     health_check_urls[proxy] = urls[proxy]["url"]["prod"]
#                 else:
#                     health_check_urls[proxy] = urls[proxy]["url"]["npe"]
#     return health_check_urls
def update_healthy_proxies(proxies):
    component_json["proxies"] = proxies
    if len(component_json["proxies"]) <= 0 and len(component_json["sharedflows"]) <= 0:
        component_json["tests"] = False
    # component_json["tests"] = False
# async def check_health(proxy, url, session):
#     try:
#         async with session.get(url=url, ssl=False) as response:
#             return {proxy: response.status}
#     except Exception as e:
#         print("Unable to get url {} due to {}.".format(url, e.__class__))
def print_status(data):
    print("{:<40} {:<15} {}".format("Proxy", "Status Code", "Deploying?"))
    for proxy, status in data.items():
        if status == 200:
            print("{:<40} {:<15} {}".format(proxy, status, "Yes"))
        else:
            print("{:<40} {:<15} {}".format(proxy, status, "No"))
def write_changed_components(data):
    with open("components.json", "w") as components:
        components.write(data)
async def main():
    branch_name = sys.argv[1]
    print("branch_name=")
    print(branch_name)
    changed_files = open("changefile.txt").read().splitlines()
    print("changed_files=")
    print(changed_files)
    healthy_proxies = []
    # urls = json.load(open("health-check.json"))
    parse_changed_components(changed_files)
    # health_check_urls = parse_health_check_urls(branch_name, urls)
    # async with aiohttp.ClientSession() as session:
    #     data = await asyncio.gather(
    #         *[
    #             check_health(proxy, url, session)
    #             for proxy, url in health_check_urls.items()
    #         ]
    #     )
    data = dict(ChainMap(*data))
    for proxy, status in data.items():
        if status == 200:
            healthy_proxies.append(proxy)
    update_healthy_proxies(healthy_proxies)
    print_status(data)
    write_changed_components(json.dumps(component_json, indent=2))
loop = asyncio.get_event_loop()
loop.run_until_complete(main())