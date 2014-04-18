<!DOCTYPE html>
<html>
  <head>
    <title>To je stran</title>
    <link rel="stylesheet" href="skin/css/style.css" type="text/css">
  </head>
  <body>
    <div class="header">
      <div style="float:right;margin-top:70px;margin-right:20px;">
        %if loggedin:
          <a href="logout">Odjava</a>
        %end
      </div>
    </div>
    <div class="content">
      {{!base}}
    </div>
  
  </body>
</html>
