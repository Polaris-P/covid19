var all = echarts.init(document.querySelector('.all'));
var allOption;
allOption = {
  title: {
    text: '本省 累计确诊/治愈/死亡 趋势'
  },
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['确诊','治愈','死亡']
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
      name:'确诊',
      data: [],
      type: 'line',
      smooth: true
    },
    {
        name:'治愈',
        data: [],
        type: 'line',
        smooth: true
    },
    {
        name:'死亡',
        data: [],
        type: 'line',
        smooth: true
    }
  ]
};