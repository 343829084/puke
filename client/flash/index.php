<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>聊天室
</title>
	<!-- Le styles -->
    <link href="bootstrap/css/bootstrap.min.css" rel="stylesheet">
    <link href="bootstrap/css/bootstrap-responsive.min.css" rel="stylesheet">

	<link rel="stylesheet" href="codemirror/lib/codemirror.css">
    <script src="codemirror/lib/codemirror.js"></script>
    <script src="codemirror/addon/edit/matchbrackets.js"></script>
    <script src="codemirror/mode/python/python.js"></script>
	<link rel="stylesheet" href="codemirror/theme/cobalt.css">
    <style type="text/css">.CodeMirror {border-top: 1px solid black; border-bottom: 1px solid black; height: auto; width: 700px}</style>
</head>
<body align='left'>
<table border="0" align="left">
  <tr>
    <th  align="center">聊天室Flash客户端</th>
    <th>聊天室服务器Python代码</th>
  </tr>
  <tr>
    <td valign="top"><embed src="chat.swf" width="600" height="600"></embed></td>
    <td><button type="button" id="butt" class="btn btn-primary">保存代码</button> 
    	<strong><font color="#ff0000">修改python代码后点击保存代码按钮，在flash聊天界面中输入reload重载脚本</font></strong></br></br>
		<textarea id="code_content"  rows="30" cols="200"><?php
		$kv = new SaeKV();
		$ret = $kv->init();
		echo $kv->get('main.py');
		?>
		</textarea></td>
  </tr>

</table>



<script>
      
    </script>
</body>

<script type="text/javascript" src="./js/jquery.js"></script>

<script>

$(document).ready( function() {
	var editor = CodeMirror.fromTextArea(document.getElementById("code_content"), {
						mode: {name: "python",
							   version: 2,
							   singleLineStringErrors: false},
						lineNumbers: true,
						indentUnit: 4,
						tabMode: "shift",
						matchBrackets: true
					  });
	editor.setOption("theme", "cobalt");
    $('#butt').click(function(){
			//data = $('#code_content').val();
			$.post("output.php", {"code":editor.getValue()}, function(result){alert(result);});
	});
});
</script>