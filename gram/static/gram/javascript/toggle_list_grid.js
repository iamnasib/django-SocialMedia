function grid(){
    var grid = document.getElementById("grid");
    var list = document.getElementById("list");
    list.style.display="none";
    grid.style.display="block";
}
function list(){
    var grid = document.getElementById("grid");
    var list = document.getElementById("list");
    grid.style.display="none";
    list.style.display="block";
}
function findPos(obj) {
	var curleft = curtop = 0;
    if (obj.offsetParent) {
        do {
			curleft += obj.offsetLeft;
			curtop += obj.offsetTop;
        }
        while (obj = obj.offsetParent);
        return [curleft,curtop];
    }
}
function postclick(id){
    var grid = document.getElementById("grid");
    var list = document.getElementById("list");
    grid.style.display="none";
    list.style.display="block";
    // document.querySelector("post"+id).scrollIntoView({
    //     behavior: 'smooth'
    //   });
    // var rect = element.getBo
    // window.scroll(0,findPos(document.getElementById("post"+id)));
    document.getElementById("post"+id).scrollIntoView({
        behavior: 'auto'
    });
    // window.scroll(0,findPos(document.getElementById("post"+id)));
}