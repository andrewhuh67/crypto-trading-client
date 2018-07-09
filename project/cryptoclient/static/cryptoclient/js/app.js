jQuery(document).ready(function() {
	
	// var closeData = {}
	$.ajax({
        type: "GET",
        url: "data",
        dataType: "json",
        success: function(data) {
        	console.log(data)
        	var chart = c3.generate({
	    		bindto: '#chart',
	    		data: {
	    			columns: [
	       				data['ltc'],
	        			// ['data2', 50, 20, 10, 40, 15, 25, 200]
	      			]
	    		}
			});

        }
    });

});