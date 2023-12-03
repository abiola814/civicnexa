

function showPage1(){
    document.getElementById('page1').style.display='block'
    document.getElementById('page3').style.display='none'
    document.getElementById('page2').style.display='none'
}
function showPage2(){
    document.getElementById('page3').style.display='none'
    document.getElementById('page1').style.display='none'
    document.getElementById('page2').style.display='block'
}
function showPage3(){
    document.getElementById('page3').style.display='block'
    document.getElementById('page1').style.display='none'
    document.getElementById('page2').style.display='none'
}