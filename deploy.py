import json
import os
import sys
import glob

PROFILE = sys.argv[1]
ORG = sys.argv[2]
APIGEE_USERNAME = sys.argv[3]
APIGEE_PASSWORD = sys.argv[4]
OPTIONS = sys.argv[5]
OVERRIDE_DELAY = sys.argv[6]
DELAY = sys.argv[7]
# COMPONENT_JSON = '{ "kvms": false, "targetServers": false, "sharedflows": [ ], "proxies":[ "echo" ], "apiProducts": false, "developers": false, "apps": false, "tests": false }'
# load components json
try:
    # loading components json from build parameters
    with open('components.json') as components:
        data = json.load(components)
        print("data=")
        print(data)
    print("Using Component Config based on repo json")
except:
    sys.exit("Error! Please Check the Component json argument")

kvms = (data["kvms"])
targetServers = (data["targetServers"])
sharedflows = (data["sharedflows"])
proxies = (data["proxies"])
apiProducts = (data["apiProducts"])
developers = (data["developers"])
apps = (data["apps"])
tests = (data["tests"])

if kvms == True:
    os.chdir("config")
    os.system('mvn apigee-config:kvms -P' + PROFILE + ' -Dusername=' + APIGEE_USERNAME + ' -Dpassword=' +
              APIGEE_PASSWORD + ' -Dorg=' + ORG + ' -Dapigee.config.options=update -Dapigee.config.dir=.')
    os.chdir("..")

if targetServers == True:
    os.chdir("config")
    os.system('mvn apigee-config:targetservers -P' + PROFILE + ' -Dusername=' + APIGEE_USERNAME + ' -Dpassword=' +
              APIGEE_PASSWORD + ' -Dorg=' + ORG + ' -Dapigee.config.options=create -Dapigee.config.dir=.')
    os.chdir("..")

for x in sharedflows:
    os.chdir("sharedflows/%s" % x)
    os.system('mvn install -P' + PROFILE + ' -Dusername=' + APIGEE_USERNAME + ' -Dpassword=' + APIGEE_PASSWORD +
              ' -Dorg=' + ORG + ' -Doptions=' + OPTIONS + ' -Doverride_delay=' + OVERRIDE_DELAY + ' -Ddelay=' + DELAY)
    os.chdir("../..")

for x in proxies:
    os.chdir("proxies/%s" % x)
    os.system('mvn install -P' + PROFILE + ' -Dusername=' + APIGEE_USERNAME + ' -Dpassword=' + APIGEE_PASSWORD +
              ' -Dorg=' + ORG + ' -Doptions=' + OPTIONS + ' -Doverride_delay=' + OVERRIDE_DELAY + ' -Ddelay=' + DELAY)
    os.chdir("../..")

if apiProducts == True:
    os.chdir("config")
    os.system('mvn apigee-config:apiproducts -P' + PROFILE + ' -Dusername=' + APIGEE_USERNAME + ' -Dpassword=' +
              APIGEE_PASSWORD + ' -Dorg=' + ORG + ' -Dapigee.config.options=create -Dapigee.config.dir=.')
    os.chdir("..")

if developers == True:
    os.chdir("config")
    os.system('mvn apigee-config:developers -P' + PROFILE + ' -Dusername=' + APIGEE_USERNAME + ' -Dpassword=' +
              APIGEE_PASSWORD + ' -Dorg=' + ORG + ' -Dapigee.config.options=create -Dapigee.config.dir=.')
    os.chdir("..")

if apps == True:
    os.chdir("config")
    os.system('mvn apigee-config:apps -P' + PROFILE + ' -Dusername=' + APIGEE_USERNAME + ' -Dpassword=' +
              APIGEE_PASSWORD + ' -Dorg=' + ORG + ' -Dapigee.config.options=create -Dapigee.config.dir=.')
    os.chdir("..")

if tests == True:
    for collection in glob.iglob("tests/*.postman_collection.json"):
        os.system('newman run ' + collection + ' --global-var "org=' + ORG + '" --global-var "env=' + PROFILE + '"')
