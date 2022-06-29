//本土新增趋势    
var localConfirmAdd =  echarts.init(document.querySelector('.localConfirmAdd'));
var localOption;
localOption = {
  title: {
    text: '新增本土趋势'
  },
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['新增本土']
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
      name:'新增本土:',
      data: [],
      type: 'line',
      smooth: true
    }
  ]
};
// localOption && localConfirmAdd.setOption(localOption);