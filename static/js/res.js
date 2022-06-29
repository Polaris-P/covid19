function confirmMap_data() {
    $.ajax({
        url:"http://127.0.0.1:5000/confirmmap",
        success: function(data) {
			conMapOption.series[0].data=data.data
            conMapOption.series[0].data.push({
      	        name:"南海诸岛",value:0,
      	        itemStyle:{
      		        normal:{ opacity:1},
      	        },
      	        label:{show:true}
            })
            confirmMap.setOption(conMapOption)
		},
		error: function(xhr, type, errorThrown) {

		}
    })
}
confirmMap_data();
 

function conAddMap_data() {
    $.ajax({
        url:"http://127.0.0.1:5000/caddmap",
        success: function(data) {
			conAddMapOption.series[0].data=data.data
            conAddMapOption.series[0].data.push({
      	        name:"南海诸岛",value:0,
      	        itemStyle:{
      		        normal:{ opacity:1},
      	        },
      	        label:{show:true}//显示南海诸岛小地图
            })
            conAddMap.setOption(conAddMapOption)
		},
		error: function(xhr, type, errorThrown) {

		}
    })
}
conAddMap_data();

function local_data(){
    $.ajax({
        // type: "get",
        url: "http://127.0.0.1:5000/localdata",
        
        dataType: "json",
        success: function (data) {
            console.log(data);
            localOption.xAxis.data=data.date;
            localOption.series[0].data=data.localConfirm_add;
            localConfirmAdd.setOption(localOption);
        }
    });
    
}
local_data();

function imp_data(){
    $.ajax({
        // type: "get",
        url: "http://127.0.0.1:5000/impdata",
        
        dataType: "json",
        success: function (data) {
            console.log(data);

            impOption.xAxis.data=data.date;
            impOption.series[0].data=data.importedCase_add;
            importedCaseAdd.setOption(impOption);
        }
    });
    
}
imp_data();

function new_data(){
    $.ajax({
        // type: "get",
        url: "http://127.0.0.1:5000/newdata",
        
        dataType: "json",
        success: function (data) {
            console.log(data);
 
            newOption.xAxis.data=data.date;
            newOption.series[0].data=data.confirm;
            newOption.series[1].data=data.importedCase_add;
            newAdd.setOption(newOption);
        }
    });
    
}
new_data();

function no_data(){
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
    
}
no_data();

function heal_data(){
    $.ajax({
        // type: "get",
        url: "/healdata",
        
        dataType: "json",
        success: function (data) {
            console.log(data);
            
            healOption.xAxis.data=data.date;
            healOption.series[0].data=data.heal;
            healOption.series[1].data=data.dead;
            healAndDead.setOption(healOption);


        }
    });
    
}
heal_data();

