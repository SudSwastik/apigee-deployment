var proxy_name=context.getVariable("apiproxy.name");
print("proxy_name="+proxy_name);
var skip_allow_proxylist = context.getVariable('apiproduct.skip_allow_list');

print(skip_allow_proxylist);


var is_allow_listed ;
context.setVariable('is_allow_listed', "false");

if(skip_allow_proxylist.indexOf(proxy_name) < -1) {
    if (context.getVariable('apiproduct.allow_list') !== null){
        var allow_list;
        allow_list = context.getVariable('apiproduct.allow_list').split(";");
        print("array of allow_list==>"+JSON.stringify(allow_list));
    
        for (var i = 0; i < allow_list.length; i++) {
        print(allow_list[i]);
        }
        var filter_var = context.getVariable('request.verb') + ":" + context.getVariable('proxy.basepath') + context.getVariable('proxy.pathsuffix');
        print("filter_var="+filter_var);
    
        for (var i = 0; i < allow_list.length; i++) {
            var re = new RegExp(allow_list[i]);
            print("i="+i+"   reg="+re);
            if(re.test(filter_var) === true) {
            print("match="+i+"   reg="+re);
            print("allowed");
            context.setVariable('is_allow_listed', "true");
            break;
            }
        }
    }
}
// print('apiproduct.allow_list='+allow_list);
print('proxy.pathsuffix='+context.getVariable('proxy.pathsuffix'));
print(context.getVariable('proxy.basepath'));
