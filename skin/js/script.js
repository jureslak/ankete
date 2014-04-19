$(document).ready( function(){
  $("#urejanje_ozadje").click( function(e){
    if (e.target == this){
      zapri();
    }
  });
});

function uredi(n){
  $("#urejanje_ozadje").show();
  $("#id_vprasanje").text(n);
  tip = $("#vprasanje"+n).attr("data-tip");
  switch (tip){
    case "text":
      htmlString = '<form action=""> Vprasanje: <input type="text" value="'+$("#vprasanje"+n+"_text").text()+'"/> </form>';
      break;
  
  }
  $("#urejanje_placeholder").html(htmlString);
}

function zapri(){
  $("#urejanje_ozadje").hide();
}
