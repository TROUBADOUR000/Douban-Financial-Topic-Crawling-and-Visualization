function get_echarts_3_data() {
    $.ajax({
        url: "/echarts_3",
        success: function (data) {
            ec_3_option.yAxis.data = data.data0;
            ec_3_option.series[0].data = data.data1;
            Chart3.setOption(ec_3_option);
        },
        error: function () {

        }
    })
}


function get_echarts_4_data() {
    $.ajax({
        url: "/echarts_4",
        success: function (data) {
            ec_4_option.xAxis.data=data.year;
            ec_4_option.series[0].data=data.p;
            ec_4_option.series[1].data=data.n;
            Chart4.setOption(ec_4_option);
        },
        error: function () {

        }
    });
}


function get_echarts_5_data() {
    $.ajax({
        url: "/echarts_5",
        success: function (data) {
            ec_5_option.series[0].data=data.data;
            Chart5.setOption(ec_5_option);
        },
        error: function () {

        }
    })
}


function get_echarts_6_data() {
    $.ajax({
        url: "/echarts_6",
        success: function (data) {
            ec_6_option.series[0].data=[]
            ec_6_option.series[0].data.push(data.data[0])
            ec_6_option.series[0].data.push(data.data[1])
            Chart6.setOption(ec_6_option);
        },
        error: function () {

        }
    })
}


function get_wordcloud_data() {
    $.ajax({
        url: "/echarts_1",
        success: function (data) {
        ec_1_option.series[0].data=data.data;
        Chart1.setOption(ec_1_option);
        },
        error: function () {

        }
    });
}


function get_pie_data() {
    $.ajax({
        url: "/echarts_2",
        success: function (data) {
        ec_2_option.series[0].data=data.data;
        Chart2.setOption(ec_2_option);
        },
        error: function () {

        }
    });
}

function get_china_map(){
    $.ajax({
        url: "/china_map",
        success: function (data) {
        ec_center_option.series[0].data=data.data;
        ec_center.setOption(ec_center_option);
        },
        error: function () {

        }
    });
    
}

get_wordcloud_data();
get_echarts_3_data();
get_echarts_4_data();
get_echarts_5_data();
get_echarts_6_data();
get_pie_data();
get_china_map();