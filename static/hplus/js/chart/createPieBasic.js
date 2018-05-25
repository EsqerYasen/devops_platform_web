


function createPieBasic(data,initConfig) {
  var names = [];
  var total = 0;
  for(var i=0;i<data.length;i++){
    total+=data[i].value;
    names.push({name:data[i].name,icon:'circle'})
  }

  var byId = echarts.init(document.getElementById(initConfig.elementId));
  var  option = {
    total:total,
    legend: {
      data:names,
      orient: 'vertical',
      x: '50%',
      y:"center",
      selectedMode:false,
      textStyle:{
        color:'rgba(0,0,0,1)',
        fontFamily:'Microsoft Yahei'
      }
    },
    title: {
      text: initConfig.title,
      left: 'center',
      bottom: '10',
      textStyle: {
        color: '#ff0000'
      }
    },
    tooltip : {
      trigger: 'item',
      formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    visualMap: {
      show: false,
      min: 600,
      max: 600,
      inRange: {
        colorLightness: [0, 1]
      }
    },
    series : [
      {
        name:'访问来源',
        type:'pie',
        radius : '70%',
        center: ['30%', '50%'],
        data:data,
        label:false,
        labelLine: false,
        itemStyle: {
          normal: {
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        },
        animationType: 'scale',
        animationEasing: 'elasticOut',
        animationDelay: function (idx) {
          return Math.random() * 100;
        }
      }
    ]
  };
  byId.setOption(option);
}


