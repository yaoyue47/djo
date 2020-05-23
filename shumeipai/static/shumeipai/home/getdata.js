function getdata(num,wendu_or_shidu){
	url = "api/get_excel_data/?page="+num +"&shumeipai_name="+shumeipai_name
	$.post(url,{

		},function(data,status){
				if(wendu_or_shidu=="wendu"){
						for(var i = 0; i < 6;i++) {
							if(data[i]!=undefined&&data[i+1]!=undefined){
								document.getElementById("wtime" + i).innerHTML = data[i]["time"];
								document.getElementById("wdata" + i).innerHTML = data[i]["temperature"];
								document.getElementById("wdis" + i).innerHTML = (data[i]["temperature"] - data[i + 1]["temperature"]).toFixed(2);
							}else {
								document.getElementById("wtime" + i).innerHTML = '无数据';
								document.getElementById("wdata" + i).innerHTML = '无数据';
								document.getElementById("wdis" + i).innerHTML = '无数据';
							}
						}
				}
				if(wendu_or_shidu=="shidu"){
					for(var i = 0; i < 6;i++) {
							if(data[i]!=undefined&&data[i+1]!=undefined){
								document.getElementById("stime" + i).innerHTML = data[i]["time"];
								document.getElementById("sdata" + i).innerHTML = data[i]["humidity"];
								document.getElementById("sdis" + i).innerHTML = (data[i]["humidity"] - data[i + 1]["humidity"]).toFixed(2);
							}else {
								document.getElementById("stime" + i).innerHTML = '无数据';
								document.getElementById("sdata" + i).innerHTML = '无数据';
								document.getElementById("sdis" + i).innerHTML = '无数据';
							}
						}
				}
				
			});
}