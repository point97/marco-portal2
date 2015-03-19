/**
Quick jquery extension for jsonrpc. 

Usage: 

$.jsonrpc('method.name', [1, 2, "Hi"], {
    success: function(success / *, full_response * /) {
        console.log("Good stuff happened", success);
    },
    error: function(error / *, full_response * /) {
        console.log("Bad Stuff happened", error);
    },
    complete: function() {
        console.log("It's all done.");
    }
});

SRH 16-Mar-2015
*/
(function($, undefined) {

function jsonrpc_call(method, args, options) {
    options = options || {};
    
    function parse_response(rpc_response, status /*, xhr*/) {
        if (rpc_response.jsonrpc != '2.0') {
            console.error("RPC Fault: bad version", rpc_response);
            return; 
        }
        
        if (rpc_response.id != 7) {
            console.error("RPC Fault: bad ID", rpc_response);
            return; 
        }
        
        var has_error = rpc_response.error && (rpc_response.error != null);
        var has_result = rpc_response.result && (rpc_response.result != null);
        
        if (has_result && !has_error) {
            if (options.success) {
                options.success(rpc_response.result, rpc_response);
            }
        }
        else if (has_error && !has_result) {
            if (options.error) {
                options.error(rpc_response.error, rpc_response);
            }
        }
        // else: if both have a result, it's an rpc fault. 
        // otherwise there was no return value (a jsonrpc command)

    }
    
    request = {
        'jsonrpc': '2.0',
        'method': method,
        'params': args || [],
        'id': 7
    };
    request_encoded = JSON.stringify(request);
        
    $.ajax({
        url: '/visualize/api', 
        method: 'POST',
        data: request_encoded, 
        dataType: 'json',
        contentType: 'application/json',
        success: parse_response,
        error: parse_response,
        complete: function() {
            if (options.complete) {
                options.complete(); 
            }
        }
    });
}

$.extend({
    jsonrpc: jsonrpc_call
})

})(jQuery)
