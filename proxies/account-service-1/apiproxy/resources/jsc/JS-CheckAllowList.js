print("here");
print("allow_list="+allow_list+"typeof"+typeof(allow_list));
var is_allow_listed ;
context.setVariable('is_allow_listed', "false");
var allow_list = context.getVariable('allow_list');

/*
Fetches the allowed path list for all proxies which are part of the apiproduct 
*/
    
    /*Splits list into individual regex path array*/
    var allow_list;
    allow_list = context.getVariable('allow_list').split(";");
    print(allow_list);
    /*Recreate the actual request being made to the proxy*/
    var filter_var = context.getVariable('request.verb') + ":" + context.getVariable('proxy.basepath') + context.getVariable('proxy.pathsuffix');
    print(filter_var);
    /*Loop through the whole list to find a valid path which is allowed*/
    for (var i = 0; i < allow_list.length; i++) {
        var re = new RegExp(allow_list[i]);
        if(re.test(filter_var) === true) {
            /*If a valid path matches then exit the loop and allow the request to go through*/
            context.setVariable('is_allow_listed', "true");
            break;
        }
    }








