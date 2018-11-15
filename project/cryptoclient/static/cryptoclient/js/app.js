$( document ).ready(function(){
	
  		$.ajax({
			type: "GET",
			url: "data",
			dataType: "json",
			success: function(data) {
				console.log(data)
				console.log('BTC')
				var chart = c3.generate({
					bindto: '#chart',
					
					data: {
						columns: [
							data['BTC'],
						]
					}
				});
			}
		});

	$("#button_1").click(function(e) {
		e.preventDefault();
		$.ajax({
		   	type: "GET",
		    url: "Ltcdata",
		    dataType: "json",
		    success: function(data){
		    	console.log(data)
		    	console.log('LTC')
		    	var chart = c3.generate({
		    		bindto: '#chart',
		    		data: {
		    			columns: [
		    				data['LTC'],
		    			]
		    		}
		    	})
		    }
		    

		    // data: {
		    //    id: $("#button_1").val(),
		    //    access_token: $("#access_token").val()
		    // },
		    // success: function(result) {
		    //   alert('ok');
		    // },
		    // error: function(result) {
		    //   alert('error');
		    //   }
	    });
	});
		
	
	

	
})


	
	// function getChartLTC() {
		
	// 	$.ajax({
	//         type: "GET",
	//         url: "data",
	//         dataType: "json",
	//         success: function(data) {
	//         	console.log(data)
	//         	var chart = c3.generate({
	// 	    		bindto: '#chartLTC',
	// 	    		data: {
	// 	    			columns: [
	// 	       				data['LTC'],
	// 		        			// ['data2', 50, 20, 10, 40, 15, 25, 200]
	// 	      			]
	// 	    		}
	// 			});
	//         }
 //    	});
	// }
	// function getChartETH() {
		
	// 	$.ajax({
	//         type: "GET",
	//         url: "data",
	//         dataType: "json",
	//         success: function(data) {
	//         	// console.log(data)
	//         	var chart = c3.generate({
	// 	    		bindto: '#chartETH',
	// 	    		data: {
	// 	    			columns: [
	// 	       				data['ETH'],
	// 		        			// ['data2', 50, 20, 10, 40, 15, 25, 200]
	// 	      			]
	// 	    		}
	// 			});
	//         }
 //    	});
	// }
	


