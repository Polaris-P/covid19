




// 全国累计治愈，死亡趋势
var healAndDead = echarts.init(document.querySelector('.healAndDead'));
    //  4.  指定配置项和数据 




var healOption;
healOption = {
  title: {
    text: '全国 累计治愈/死亡 趋势'
  },
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['治愈','死亡']
  },
  xAxis: {
    type: 'category',
    data: []
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name:'治愈:',
      data: [],
      type: 'line',
      smooth: true
    },
    {
        name:'死亡:',
        data: [],
        type: 'line',
        smooth: true
    }
  ]
};
// healAndDead && healAndDead.setOption(healOption);


    
      




