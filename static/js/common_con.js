var add = echarts.init(document.querySelector('.add'));
var conOption;
conOption = {
  title: {
    text: '本省新增确诊趋势'
  },
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['新增确诊']
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
      name:'新增确诊:',
      data: [],
      type: 'line',
      smooth: true
    }
  ]
};