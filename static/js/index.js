

function showModal(){
    document.getElementById('modal').style.display= 'flex'
}
function closeModal(){
    document.getElementById('modal').style.display= 'none'
}

function showReceipt(){
    document.getElementById('modall').style.display= 'flex'
}
function closeModall(){
    document.getElementById('modall').style.display= 'none'
    document.getElementById('modal').style.display= 'none'
}
function showPage1(){
    document.getElementById('page1').style.display='block'
    document.getElementById('page2').style.display='none'
}
function showPage2(){
    document.getElementById('page2').style.display='block'
    document.getElementById('page1').style.display='none'
}