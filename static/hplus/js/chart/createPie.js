function createPie(data,initConfig) {
  var styleNormal= {
    formatter: ' {b|{b}} \n{hr|}\n {c|{c}}  {per|{d}%} ',
    borderWidth: 0.5,
    borderRadius: 4,
    borderColor: '#eee',
    backgroundColor: '#fefefe',
    rich: {
      a: {
        color: '#999',
        lineHeight: 18,
        align: 'center'
      },
      cda:{
        padding:[5,5,5,5]
      },
      c:{
        align: 'center',
        fontSize: 14,
        lineHeight:33,
        color:"#444"
      },
      hr: {
        borderColor: '#eee',
        width: '100%',
        borderWidth: 0.5,
        height: 0
      },
      b: {
        fontSize: 16,
        align:'center',
        color:"#444",
        padding:[5,5,5,5]
      },
      per: {
        align:'left',
        fontSize: 12,
        lineHeight:18,
        color:"#ffffff",
        backgroundColor:"#ee2c36",
        // margin:[2,2,2,2],
        padding:[3,3,3,3],
        borderRadius:3
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
      }
    ]
  };

  if(initConfig.colors){
    options.color=initConfig.colors;
  }
  byId.setOption(options);
}
