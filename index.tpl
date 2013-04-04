<!DOCTYPE html>
<!-- vim: set sts=2 sw=2 et tw=0 : -->
<html lang="en">
<meta charset="UTF-8">
<head>
	<title>Braille Converter</title>
	<link rel="stylesheet" href="static/style.css" lang="text/css" media="screen" />
  <link rel="shortcut icon" href="favicon.ico" />
</head>

<body>
    <div id="wrapper">
      <div id="content">
        <div id="header">
          <div style="text-align: left; float: left; width: 70%;"><h1>Devanagari to Bharati Braille</h1></div>
          <div id="about"><h1><a href="">About</a></h1></div>
        </div>
        <div id="text">
          <div id="input">
            <form action="" method="POST">
            <div id="input_area">
              <!-- BEGIN: Hack to make the textarea auto-resize -->
              <div class="expandingArea">
                <pre><span></span><br></pre>
                  <textarea name="devanagari" autofocus placeholder="Enter Devanagari text here">{{input_text}}</textarea>
              </div>
              <!-- Comment-out the form autoresizing on IE8 and lower -->
              <comment>
                <script type="text/javascript" src="js/expandingarea.js"></script>
                </script>
              </comment>
              <!-- END: Hack to make the textarea auto-resize -->
            </div>
            <p id="submit"><input type="submit" value="Submit"/> →</p>
            </form>
          </div>
          <div id="output">
            <div id="output_area">
              {{braille}}
            </div>
            <p id="fake_submit">&nbsp;</p>
          </div>
        </div>
      </div>
      <!-- This exists purely for the sticky footer. Keep it the last div. -->
      <div id="push"></div>
    </div>

    <div id="footer">
      <div id="footer_content">
        <p id="madeby">Made by <a href="">Pareidolic</a></p>
      </div>
    </div>
</body>
</html>
