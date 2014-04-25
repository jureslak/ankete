<!DOCTYPE html>
<html>
  <head>
    <title>To je stran</title>
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/2.1.0/jquery.min.js"></script>
    <script src="/skin/js/script.js"></script>
    <link rel="stylesheet" href="/skin/css/style.css" type="text/css">
  </head>
  <body>
    <div class="header">
      <div style="float:right;margin-top:70px;margin-right:20px;">
        %if loggedin:
          <a href="/logout/">Odjava</a>
        %end
      </div>
    </div>
    <div class="menu_placeholder">
      %if loggedin:
        % include("menu.tpl")
      %end
    </div>
    <div class="content">
      {{!base}}
    </div>
  
  </body>
</html>
