function createPie(data,initConfig) {
  var styleNormal= {
    formatter: '  {b|{b}} \n {c|{c}} \n  {per|{d}%}  ',
    borderWidth: 1,
    borderRadius: 4,
    rich: {
      a: {
        color: '#999',
        lineHeight: 22,
        align: 'center'
      },
      c:{
        align: 'center'
      },
      hr: {
        borderColor: '#aaa',
        width: '100%',
        borderWidth: 0.5,
        height: 0
      },
      b: {
        fontSize: 16,
        lineHeight: 33,
        align:'center'
      },
      per: {
        align:'center'
      }
    }
  };
  var total = 0;
  var titleo = {
    textStyle: {
      fontSize: 14,
      color:"#666"
    }
  };
  var byId = echarts.init(document.getElementById(initConfig.elementId));
  for(var i=0;i<data.length;i++){
    total+=data[i].value;
  }
  if(initConfig.title){
    titleo.text=initConfig.title;
    titleo.top="bottom";
    titleo.left='center';
  }
  var options = {
    title:titleo,
    graphic:{
      type:'text',
      left:'center',
      top:'center',
      z:2,
      style:{
        text:'Total:'+total,
        width:100,
        height:100,
        fontSize:16
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: " {b}: {c} ({d}%)"
    },
    series: [
      {
        name:'',
        type:'pie',
        radius: ['40%', '60%'],
        label: {
          normal: styleNormal
        },
        data:data
//
      }
    ]
  };

  if(initConfig.colors){
    options.color=initConfig.colors;
  }
  byId.setOption(options);
}
