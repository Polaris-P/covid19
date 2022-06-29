let a=window.location.pathname;
let b=decodeURIComponent(a)
console.log(b)

function provinceData(){
    let url1="http://127.0.0.1:5000/provincedata"
    provinceName=['台湾','上海','香港','北京','四川','河南','天津','福建','吉林','广东','云南','浙江','青海', '山东','辽宁', '广西','江苏','河北'
    ,'湖南','贵州','黑龙江','江西','山西','内蒙古',
    '陕西','甘肃','湖北','海南','澳门','新疆','安徽','宁夏','西藏','重庆']

    for (var i = 0; i <provinceName.length; i++) {
        url2="/"+provinceName[i]
        if(url2==b){
            $.ajax({
                url: url1+url2,
                dataType: 'json',
                success: function(data){
                    console.log(data);
                    conOption.xAxis.data=data.date;
                    conOption.series[0].data=data.confirm_add;
                    add.setOption(conOption);
                    allOption.xAxis.data=data.date;
                    allOption.series[0].data=data.confirm;
                    allOption.series[1].data=data.heal;
                    allOption.series[2].data=data.dead;
                    all.setOption(allOption);
                }
            })
        } 
    }
}

provinceData()







































