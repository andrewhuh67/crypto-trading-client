$( document ).ready(function(){
	$.ajax({
			type: "GET",
			url: "data",
			dataType: "json",
			success: function(data) {
				// console.log(data)
				var chart = c3.generate({
					bindto: '#chart',
					size: {
						height:60,
						width:120
					}
					data: {
						columns: [
							data['BTC'],
						]
					}
				});
			}
		});
})

	
		
		// $.ajax({
		// 	type: "GET",
		// 	url: "data",
		// 	dataType: "json",
		// 	success: function(data) {
		// 		// console.log(data)
		// 		var chart = c3.generate({
		// 			bindto: '#chart',
		// 			data: {
		// 				columns: [
		// 					data['BTC'],
		// 				]
		// 			}
		// 		});
		// 	}
		// });
	
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
	


