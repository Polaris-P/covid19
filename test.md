##测试记录


'SELECT * FROM ' \
          '(select province,sum(confirm_add),sum(confirm),sum(heal),sum(dead) as de from details  ' \
          'where update_time=(select update_time from details ' \
          'order by update_time desc limit 1) ' \
          'group by province) as a ' \
          'ORDER BY de DESC'


'SELECT city,province,confirm_add,nowConfirm from details ORDER BY update_time desc LIMIT 60'

'SELECT confirm,importedCase,heal,dead from history ORDER BY ds desc LIMIT 1'

'SELECT * FROM ' \
          '(select province,sum(confirm_add),update_time as de from details  ' \
          'where province="澳门" ' \
          'group by update_time) as a ' \
          'ORDER BY de DESC limit 10'


<table class="table table-hover city">
                    <tr>
                        <th>地区</th>
                        <th>新增确诊</th>
                        <th>现有确诊</th>
                    </tr>
                    {% for city_data in city_data %}
                    <tr class="cityData">
                        
                            <th><a href="#">{{city_data[0]}}<span>{{city_data[1]}}</span></a></th>
                        
                            <th>{{city_data[2]}}</th>
                            <th>{{city_data[3]}}</th>
                            
                        
                    </tr>
                    {% endfor %}
</table>




function con(){
    let b = window.location.pathname;
    let a = decodeURIComponent(b);
    switch(b){
        case a=="/北京":
            $.ajax({
                // type: "get",
                url: "http://127.0.0.1:5000/jxcon",
                
                dataType: "json",
                success: function (data) {
                    console.log(data);
                    conOption.xAxis.data=data.date;
                    conOption.series[0].data=data.confirm_add;
                    add.setOption(conOption);
                }
            });
            break;
        case a=="/天津":
            $.ajax({
                // type: "get",
                url: "/tjcon",
                
                dataType: "json",
                success: function (data) {
                    console.log(data);
                    noOption.xAxis.data=data.date;
                    noOption.series[0].data=data.confirm;
                    noOption.series[1].data=data.nowConfirm;
                    noOption.series[2].data=data.noInfect;
                    noInAndCon.setOption(noOption);
                }
            });
            break;
        case a=="/上海":
            $.ajax({
                // type: "get",
                url: "http://127.0.0.1:5000/nodata",
                
                dataType: "json",
                success: function (data) {
                    console.log(data);
                    noOption.xAxis.data=data.date;
                    noOption.series[0].data=data.confirm;
                    noOption.series[1].data=data.nowConfirm;
                    noOption.series[2].data=data.noInfect;
                    noInAndCon.setOption(noOption);
                }
            });
            break;
        case a=="/重庆":
            break;
        case a=="/安徽":
            break;
        case a=="/福建":
            break;
        case a=="/广东":
            break;
        case a=="/广西":
            break;
        case a=="/贵州":
            break;
        case a=="/甘肃":
            break;
        case a=="/海南":
            break;
        case a=="/河南":
            break;
        case a=="/黑龙江":
            break;
        case a=="/湖北":
            break;
        case a=="/湖南":
            break;
        case a=="/河北":
            break;
        case a=="/江苏":
            break;
        case a=="/江西":
            break;
        case a=="/吉林":
            break;
        case a=="/辽宁":
            break;
        case a=="/宁夏":
            break;
        case a=="/内蒙古":
            break;
        case a=="/青海":
            break;
        case a=="/山东":
            break;
        case a=="/山西":
            break;
        case a=="/陕西":
            break;
        case a=="/四川":
            break;
        case a=="/台湾":
            break;
        case a=="/西藏":
            break;
        case a=="/新疆":
            break;
        case a=="/云南":
            break;
        case a=="/浙江":
            break;
        case a=="/香港":
            break;
        case a=="/澳门":
            break;
        

    }
}
con();