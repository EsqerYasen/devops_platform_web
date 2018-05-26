function createPie(data,initConfig) {

  var names=[];
  var  total = 0;
  var  titleo = {
    textStyle: {
      fontSize: 14,
      color:"#666"
    }
  };

  var byId = echarts.init(document.getElementById(initConfig.elementId));


  for(var i=0;i<data.length;i++){
    total+=data[i].value;
    names.push(data[i].name)
  }
  if(initConfig.title){
    titleo.text=initConfig.title;
    titleo.top="10";
    titleo.left='center';
  }

  var options = {

    total:total,
    title:titleo,
    graphic:{
      type: 'group',
      id: 'textGroup1',
      left: '15%',
      top: 'center',
      bounding: 'raw',
      children: [
        {
          type: 'rect',
          left: 'center',
          top: 'center',
          shape: {
            width: 75,
            height: 55
          },
          style: {
            fill: null,
          }
        },
        {
          type: 'text',
          z: 100,
          top: 'middle',
          left: 'center',
          style: {
            text: [
              'Total:'+total
            ].join('\n'),
            font: '14px "STHeiti", sans-serif'
          }
        }
      ]
    },

    tooltip: {
      trigger: 'item',
      formatter: " {b}: {c} ({d}%)"
    },
    legend: {
      data:names,
      orient: 'vertical',
      x: '30%',
      y:"center",
      selectedMode:false,
      textStyle:{
        color:'rgba(0,0,0,1)',
        fontFamily:'Microsoft Yahei'
      }
    },
    series: [
      {
        name:'',
        type:'pie',
        radius: [50, 70],
        center: ['15%', '50%'],
        label:false,
        labelLine: false,
        data:data
      }
    ]

  };

  if(initConfig.colors){
    options.color=initConfig.colors;
  }
  byId.setOption(options);
}
