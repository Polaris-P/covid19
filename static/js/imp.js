// 新增境外趋势
var importedCaseAdd = echarts.init(document.querySelector('.importedCaseAdd'));
var impOption;
impOption = {
  title: {
    text: '境外输入新增趋势'
  },
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['新增境外输入']
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
      name:'新增境外输入:',
      data: [],
      type: 'line',
      smooth: true
    }
  ]
};
// impOption && importedCaseAdd.setOption(impOption);