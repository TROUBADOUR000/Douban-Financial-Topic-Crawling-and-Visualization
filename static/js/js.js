/*   */
$(window).load(function () {
  $(".loading").fadeOut()
})
$(function () {
  echarts_1();
  echarts_2();
  echarts_3();
  echarts_4();
  echarts_5();
  //echarts_7();
  echarts_6();
  ChinaMap();

  function echarts_1() {
    Chart1 = echarts.init(document.getElementById('echart1'));
    ec_1_option = {
      tooltip: {
        trigger: 'item',
        formatter: "{b} : {c} %"
      },

      series: [{
        type: 'wordCloud',
        shape: 'circle',
        gridSize: 1,
        sizeRange: [12, 55],  //画布范围，如果设置太大会出现少词（溢出屏幕）
        rotationRange: [-45, 0, 45, 90],  //数据翻转范围
        textStyle: {
          normal: {
            color: function () { // 添加随机颜色
              return 'rgb(' +
                Math.round(Math.random() * 200) +
                ',' + Math.round(100 + Math.random() * (250 - 100)) +
                ',' + Math.round(100 + Math.random() * (250 - 100)) + ')'
            }
          }
        },
        right: null,
        bottom: null,
        data: []

      }]
    };

    // 使用刚指定的配置项和数据显示图表。
    Chart1.setOption(ec_1_option);
    window.addEventListener("resize", function () {
      Chart1.resize();
    });
  }

  function echarts_2() {
    Chart2 = echarts.init(document.getElementById('echart2'));
    ec_2_option = {
      tooltip: {
        trigger: 'item'
      },
      legend: {
        top: '0%',
        left: 'left'
      },
      series: [
        {
          name: '对待金融市场态度比例(%)',
          type: 'pie',
          radius: ['40%', '70%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderWidth: 2
          },
          label: {
            show: false,
            position: 'center'
          },
          emphasis: {
            label: {
              show: true,
              fontSize: 40,
              fontWeight: 'bold'
            }
          },
          labelLine: {
            show: false
          },
          data: []
        }
      ]
    };

    // 使用刚指定的配置项和数据显示图表。
    Chart2.setOption(ec_2_option);
    window.addEventListener("resize", function () {
      Chart2.resize();
    });
  }

  function echarts_3() {
    Chart3 = echarts.init(document.getElementById('echart3'));
    ec_3_option = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          // Use axis to trigger tooltip
          type: 'shadow' // 'shadow' as default; can also be 'line' or 'shadow'
        }
      },
      legend: {},
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'value'
      },
      yAxis: {
        type: 'category',
        data: []
      },
      series: [
        {
          name: '文章数目',
          type: 'bar',
          stack: 'total',
          label: {
            show: false
          },
          emphasis: {
            focus: 'series'
          },
          data: []
        }
      ]
    };
    // 使用刚指定的配置项和数据显示图表。
    Chart3.setOption(ec_3_option);
    window.addEventListener
      (
        "resize", function () {
          Chart3.resize();
        }
      );
  }

  function echarts_4() {
    Chart4 = echarts.init(document.getElementById('echart4'));
    ec_4_option = {
      tooltip: {
        trigger: 'axis'
      },
      legend: {},
      toolbox: {
        show: true,
        feature: {
          dataZoom: {
            yAxisIndex: 'none'
          },
          dataView: { readOnly: false },
          magicType: { type: ['line', 'bar'] },
          restore: {},
          saveAsImage: {}
        }
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: []
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          name: '积极',
          type: 'line',
          data: [],
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
          markLine: {
            data: [{ type: 'average', name: 'Avg' }]
          }
        },
        {
          name: '消极',
          type: 'line',
          data: [],
          markPoint: {
            data: [
              { type: 'max', name: 'Max' },
              { type: 'min', name: 'Min' }
            ]
          },
          markLine: {
            data: [{ type: 'average', name: 'Avg' }]
          }
        }
      ]
    };
    // 使用刚指定的配置项和数据显示图表。
    Chart4.setOption(ec_4_option);
    window.addEventListener(
      "resize", function () {
        Chart4.resize();
      });
  }


  function echarts_5() {
    Chart5 = echarts.init(document.getElementById('echart5'));
    ec_5_option = {
      tooltip: {
        trigger: 'item',
        formatter: "{b} : {c} %"
      },

      series: [{
        type: 'wordCloud',
        shape: 'circle',
        gridSize: 1,
        sizeRange: [12, 55],  //画布范围，如果设置太大会出现少词（溢出屏幕）
        rotationRange: [-45, 0, 45, 90],  //数据翻转范围
        textStyle: {
          normal: {
            color: function () { // 添加随机颜色
              return 'rgb(' +
                Math.round(Math.random() * 155) +
                ',' + Math.round(100 + Math.random() * (250 - 100)) +
                ',' + Math.round(100 + Math.random() * (250 - 100)) + ')'
            }
          }
        },
        right: null,
        bottom: null,
        data: []

      }]
    };

    // 使用刚指定的配置项和数据显示图表。
    Chart5.setOption(ec_5_option);
    window.addEventListener("resize", function () {
      Chart5.resize();
    });
  }

  function ChinaMap() {
    ec_center = echarts.init(document.getElementById('echarts_map'));

    ec_center_option = {
      title: {
        text: '',
        subtext: '',
        x: 'left'
      },
      tooltip: {
        trigger: 'item'
      },
      //左侧小导航图标
      visualMap: {
        show: true,
        x: 'left',
        y: 'bottom',
        textStyle: {
          fontSize: 8,
        },
        splitList: [{ start: 1, end: 9 },
        { start: 10, end: 20 },
        { start: 20, end: 30 },
        { start: 30, end: 40 },
        { start: 40 }],
        color: ['#8A3310', '#C64918', '#E55B25', '#F2AD92', '#F9DCD1']
      },
      //配置属性
      series: [{
        name: '人数',
        type: 'map',
        mapType: 'china',
        roam: false, //拖动和缩放
        itemStyle: {
          normal: {
            borderWidth: .5, //区域边框宽度
            borderColor: '#009fe8', //区域边框颜色
            areaColor: "#ffefd5", //区域颜色
          },
          emphasis: { //鼠标滑过地图高亮的相关设置
            borderWidth: .5,
            borderColor: '#4b0082',
            areaColor: "#fff",
          }
        },
        label: {
          normal: {
            show: true, //省份名称
            fontSize: 8,
          },
          emphasis: {
            show: true,
            fontSize: 8,
          }
        },
        data: [] //mydata //数据
      }]
    };
    ec_center.setOption(ec_center_option)
    window.addEventListener("resize", function () {
      ec_center.resize();
    });
  }

  function echarts_6() {
    Chart6 = echarts.init(document.getElementById('echart6'));
    ec_6_option = {
      tooltip: {
        trigger: 'item',
        axisPointer: {
          type: 'shadow'
        }
      },
      grid: {
        left: '15%',
        right: '10%',

      },
      xAxis: {
        type: 'category',
        data: ['积极', '消极'],

        nameTextStyle: {
          color: '#3259B8',
          fontSize: 14,

        },
        axisTick: {
          show: false,
        },
        axisLine: {
          lineStyle: {
            color: '#3259B8',
          }
        },
        splitLine: {
          show: false
        }
      },

      yAxis: {
        type: 'value',
        nameTextStyle: {
          color: '#3259B8',
          fontSize: 14,
        },
        axisLabel: {
          formatter: '{value}',
        },
        axisTick: {
          show: false,
        },
        axisLine: {
          lineStyle: {
            color: '#3259B8',
          }
        },
        splitLine: {
          lineStyle: {
            color: '#A7BAFA',
          },
        }

      },
      series: [{
        name: 'boxplot',
        type: 'boxplot',
        data: [
          [30645,
            54699,
            66480,
            86502,
            159424,],
          [19747,
            47590,
            60778,
            85884,
            159949,],
          [15202,
            40968.5,
            52101,
            77910.75,
            159978,],
        ],
        itemStyle: {
          normal: {
            borderColor: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 0,
              y2: 1,
              colorStops: [{
                offset: 0,
                color: '#F02FC2' // 0% 处的颜色
              }, {
                offset: 1,
                color: '#3EACE5' // 100% 处的颜色
              }],
              globalCoord: false // 缺省为 false
            },
            borderWidth: 2,
            color: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 0,
              y2: 1,
              colorStops: [{
                offset: 0,
                color: 'rgba(240,47,194,0.7)'  // 0% 处的颜色
              }, {
                offset: 1,
                color: 'rgba(62,172,299,0.7)' // 100% 处的颜色
              }],
              globalCoord: false // 缺省为 false
            },
          }
        },
        tooltip: {
          formatter: function (param) {
            return [

              'Upper: ' + param.data[5],
              'Q3: ' + param.data[4],
              'Median: ' + param.data[3],
              'Q1: ' + param.data[2],
              'Lower: ' + param.data[1]
            ].join('<br/>')
          }
        }
      },

      ]
    };
    // 使用刚指定的配置项和数据显示图表。
    Chart6.setOption(ec_6_option);
    window.addEventListener(
      "resize", function () {
        Chart6.resize();
      });
  }

})


















