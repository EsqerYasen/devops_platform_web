  function createBar(data, initConfig){
    	var legend = [];
    	var xAxis = [];
    	var series = [];
    	var labelOption = {
		    normal: {
		        show: true,
		        position: 'insideBottom',
		        distance:  '15',
		        align: 'left',
		        verticalAlign: 'middle',
		        rotate: 90,
		        formatter: '{c}  {name|{a}}',
		        fontSize: 16,
		        rich: {
		            name: {
		                textBorderColor: '#fff'
		            }
		        }
		    }
		};
    	for(var key in data){
    		legend.push(key);
    		var serie = {
			          type: "bar",
			          label: labelOption,
			          stack:'og',
								barWidth:50,
			          data: [],//（<%=zcfgData%>为后台传过来的数据，格式为,根据实际情况修改
			          itemStyle: {
			          	normal:{
			          		color: initConfig.colors.pop()
			          	}
			      	}
			    };
    		for(var key$1 in data[key]){
    			serie.name = key;
    			if(xAxis.indexOf(key$1) === -1)xAxis.push(key$1);
    			serie.data.push(data[key][key$1]);
    		}
    		series.push( serie );
    	}
    	var app = echarts.init(document.getElementById(initConfig.elementId));


    	var option = {
			      title: {
			        text: initConfig.title || '标题',
							top:"bottom",
							left:"center",
			        textStyle: {
			          fontSize: 14,

			        }
			      },
			      //鼠标触发提示数量
			      tooltip: {
			        trigger: "axis"
			      },
			      legend: {
			        data:legend
			      },
			      //x轴显示
			      xAxis: {
			        data: xAxis,
			        splitLine:{
			          show:false
			        }
			      },
			      //y轴显示
			      yAxis: {
			        splitLine:{
			          show:true
			        }
			      },
			      series: series
    		};

    	app.setOption(option);
    }