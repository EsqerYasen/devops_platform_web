function createPie(data,initConfig) {

  var names=[];
  var  total = 0;
  var  titleo = {
    textStyle: {
      fontSize: 15,
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
      left: '20%',
      top: 'center',
      bounding: 'raw',
      children: [
        {
          type: 'rect',
          left: 'center',
          top: 'center',
          shape: {
            width: 100,
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
            font: '16px "STHeiti", sans-serif'
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
      x: '40%',
      y:"center",
      selectedMode:false,
      textStyle:{
        color:'rgba(0,0,0,1)',
        fontSize:13
      },
      formatter:  function(name){
          var total = 0;
          var target;
          for (var i = 0, l = data.length; i < l; i++) {
          total += data[i].value;
          if (data[i].name == name) {
              target = data[i].value;
              }
          }
          return name +' '+target+ '(' + ((target/total)*100).toFixed(2) + '%)';
      }
    },
    series: [
      {
        name:'',
        type:'pie',
        radius: [60, 100],
        center: ['20%', '50%'],
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
