function getechartsdata(tianshu,wendu_or_shidu,){
	var url ="api/get_echarts_data/?tianshu="+tianshu+"&shumeipai_name="+shumeipai_name
	$.post(url,{

		},function(data,status){

				if(wendu_or_shidu=="wendu"){
					option = {
						xAxis: {
							type: 'category',
							data: data.time,
							axisLabel:{
							rotate:60
							}
						},
						yAxis: {
							type: 'value',
						   // min:20
						},
						grid: {
							left: '10%',
							bottom:'35%'
						},
						series: [{
							data: data.temperature,
							type:"line",
							markPoint: {
							data: [
								{type: 'max', name: '最大值'},
								{type: 'min', name: '最小值'}
							]
						},
						}],
					};
				myChart_wendu.setOption(option);
		   		//echartd的图表
   				}
				if(wendu_or_shidu=="shidu"){
					option = {
						xAxis: {
							type: 'category',
							data: data.time,
							axisLabel:{
							rotate:60
							}
						},
						yAxis: {
							type: 'value',
						   // min:20
						},
						grid: {
							left: '10%',
							bottom:'35%'
						},
						series: [{
							data: data.humidity,
							type:"line",
							markPoint: {
							data: [
								{type: 'max', name: '最大值'},
								{type: 'min', name: '最小值'}
							]
							},
						}],
					};


				myChart_shidu.setOption(option);
				}
				if(wendu_or_shidu=="ph"){
					option = {
						xAxis: {
							type: 'category',
							data: data.time,
							axisLabel:{
							rotate:60
							}
						},
						yAxis: {
							type: 'value',
						   // min:20
						},
						grid: {
							left: '10%',
							bottom:'35%'
						},
						series: [{
							data: data.ph,
							type:"line",
							markPoint: {
							data: [
								{type: 'max', name: '最大值'},
								{type: 'min', name: '最小值'}
							]
						},
						}],
					};
				myChart_ph.setOption(option);
		   		//echartd的图表
   				}
				if(wendu_or_shidu=="sun"){
					option = {
						xAxis: {
							type: 'category',
							data: data.time,
							axisLabel:{
							rotate:60
							}
						},
						yAxis: {
							type: 'value',
						   // min:20
						},
						grid: {
							left: '10%',
							bottom:'35%'
						},
						series: [{
							data: data.sun,
							type:"line",
							markPoint: {
							data: [
								{type: 'max', name: '最大值'},
								{type: 'min', name: '最小值'}
							]
						},
						}],
					};
				myChart_sun.setOption(option);
		   		//echartd的图表
   				}

		});
}
