$(document).ready( function(){
  $("#urejanje_ozadje").click( function(e){
    if (e.target == this){
      zapri();
    }
  });
  $("#tip").change( function(){
    if ($("#tip").val() == "text"){
      if ($("#seznam").css("display")!="none") $("#seznam").hide(200);//.css("display","none");
    }
    else if ($("#tip").val() == "radiobutton"){
      if ($("#seznam").css("display")=="none") callbackPrikazSeznam();
    }
  });
});

function uredi(n){
  $("#urejanje_ozadje").show();
  $("#id_vprasanje").text(n);
  //dinamicno izbiranje pravega <optiona> v <selectu> tip
  tip = $("#vprasanje"+n).attr("data-tip");
  $("#tip > option").each( function(){
    if (this.text == tip) $(this).prop("selected", true);
  });
  //dinamicno dodajanje vrednosti "naslov"
  $("#naslov").val($("#vprasanje"+n+"_text").text());
  
  if (tip == "radiobutton"){
    callbackPrikazSeznam();
    $("#seznam").html($("#vprasanje"+n).attr("data-vprasanja"));
  }
}

function callbackPrikazSeznam()
{
  $("#seznam").show(200);
}

function zapri(){
  $("#urejanje_ozadje").hide();
  $("#seznam").css("display","none");
}
