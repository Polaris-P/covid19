// 全国新增趋势
var newAdd = echarts.init(document.querySelector('.newAdd'));
var newOption;
newOption = {
  title: {
    text: '全国 总新增确诊/新增境外输入确诊 趋势'
  },
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['总新增确诊','新增境外输入']
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
        name:'总新增确诊:',
      data: [],
      type: 'line',
      smooth: true
    },
    {
        name:'新增境外输入:',
        data: [],
        type: 'line',
        smooth: true
    }
  ]
};
// newOption && newAdd.setOption(newAdd);