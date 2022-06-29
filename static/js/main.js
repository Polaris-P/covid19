let nowCon=document.querySelector('.nowConfirmMap');
let conAdd=document.querySelector('.confirmAddMap');
let btn1 = document.querySelectorAll('.btn1');
let loAdd= document.querySelector('.localConfirmAdd');
let imAdd= document.querySelector('.importedCaseAdd');
let btn2= document.querySelectorAll('.btn2');
let newAd= document.querySelector('.newAdd');
let noCon= document.querySelector('.noInAndCon');
let hd= document.querySelector('.healAndDead');
let btn3= document.querySelectorAll('.btn3');
let spread = document.querySelectorAll('.spread');
let docer= document.querySelector('.docer');
let btn5 = document.querySelectorAll('.btn5');

for(let i=0; i<btn1.length; i++){
    btn1[i].addEventListener('click',function(){
        for(let j=0;j<btn1.length; j++){
            btn1[j].style.background="#E3E6EB";
        }
        this.style.background="#FFFFFF";
        if(i==0){
            nowCon.style.display='block';
            conAdd.style.display='none'
        }else if(i==1){
            nowCon.style.display='none';
            conAdd.style.display='block';
        }
    })
}
for(let i=0; i<btn2.length; i++){
    btn2[i].addEventListener('click',function(){
        for(let j=0;j<btn2.length; j++){
            btn2[j].style.background="#E3E6EB";
        }
        this.style.background="#FFFFFF";
        if(i==0){
            loAdd.style.display='block';
            imAdd.style.display='none'
        }else if(i==1){
            loAdd.style.display='none';
            imAdd.style.display='block';
        }
    })
}
for(let i=0; i<btn3.length; i++){
    btn3[i].addEventListener('click',function(){
        for(let j=0;j<btn3.length; j++){
            btn3[j].style.background="#E3E6EB";
        }
        this.style.background="#FFFFFF";
        if(i==0){
            newAd.style.display='block';
            noCon.style.display='none';
            hd.style.display='none';
        }else if(i==1){
            newAd.style.display='none';
            noCon.style.display='block';
            hd.style.display='none';
        }else if(i==2){
            newAd.style.display='none';
            noCon.style.display='none';
            hd.style.display='block';
        }
    })
}
for(let i=0; i<spread.length; i++){
    spread[i].addEventListener('click',function(){
        
        this.style.display='none';
        if(i==0){
            // document.querySelector('.cityData').style.display='flex'
            let city= document.querySelectorAll('.cityData')
            for(let k=0;k<city.length;k++){
                city[k].style.display='flex'
            }
        }else if(i==1){
            let pro= document.querySelectorAll('.proData')
            for(let k=0;k<pro.length;k++){
                pro[k].style.display='flex'
            }
        }else if(i==2){
            let news= document.querySelectorAll('.newsData')
            for(let k=0;k<news.length;k++){
                news[k].style.display='block'
            }
        }
    })
}

for(let i=0; i<btn5.length; i++){
  btn5[i].addEventListener('click',function(){
      for(let j=0;j<btn5.length; j++){
          btn5[j].style.color="#000";
      }
      this.style.color="#10AEB5";
      
  })
}

window.onscroll = function () {
  let topScroll = document.documentElement.scrollTop;
  let docer= document.querySelector('.docer');
  // console.log(topScroll);
  if (topScroll > 175) {
    docer.style.display = "flex";
  } else {
    docer.style.display="none";
  }
}