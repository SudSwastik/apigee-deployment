import groovy.json.JsonSlurper
import groovy.json.JsonOutput
import com.cloudbees.plugins.credentials.Credentials

def updateJSON(workspace, profile) {
    def jsonSlurper = new JsonSlurper()

    File kvmFile = new File(workspace + '/config/env/' + profile + '/kvms.json')
    def kvmJSON = jsonSlurper.parse(kvmFile)

    Set<Credentials> allCredentials = new HashSet<Credentials>()

    println('Fetching Credentials')
    def creds = com.cloudbees.plugins.credentials.CredentialsProvider.lookupCredentials(
        com.cloudbees.plugins.credentials.common.IdCredentials
    )

    allCredentials.addAll(creds)

    println('Updating KVMs')
    for (int i = 0; i < kvmJSON.size(); i++) {
        for (c in allCredentials) {
            if (kvmJSON[i]['name'] == c.id && c.properties.secret) {
                kvmJSON[i]['entry'] = jsonSlurper.parseText(c.secret.toString())
            }
        }
    }
    kvmFile.write(JsonOutput.toJson(kvmJSON))
    println('Updated KVM Entries. Ready for KVM deploy')
}

return this
