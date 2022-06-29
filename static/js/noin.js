// 全国确诊，疑似趋势
var noInAndCon = echarts.init(document.querySelector('.noInAndCon'));
var noOption;
noOption = {
  title: {
    text: '全国 现有确诊/疑似/累计确诊 趋势'
  },
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['累计确诊','现有确诊','现有疑似']
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
      name:'累计确诊',
      data: [],
      type: 'line',
      smooth: true
    },
    {
        name:'现有确诊',
        data: [],
        type: 'line',
        smooth: true
    },
    {
        name:'现有疑似',
        data: [],
        type: 'line',
        smooth: true
    }
  ]
};
// noOption && noInAndCon.setOption(noOption);