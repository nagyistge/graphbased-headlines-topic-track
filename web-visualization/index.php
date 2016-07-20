<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
	"http://www.w3.org/TR/html4/loose.dtd">
<html>
	<head>
		<title></title>
		<style> 
			.newspaper {
				-webkit-column-count: 3; /* Chrome, Safari, Opera */
				-moz-column-count: 3; /* Firefox */
				column-count: 3;
			}
		</style>
		<script src="jquery-1.11.3.min.js"></script>
		<script type="text/javascript" src="vis.js"></script>
		<link href="vis.css" rel="stylesheet" type="text/css" />
		 <style type="text/css">
			#mynetwork {
				width: 100vw;
				height: 100vh;
				border: 1px solid #444444;
				background-color: #222222;
			}
			#loadingBar {
            position:absolute;
            top:0px;
            left:0px;
            width: 902px;
            height: 902px;
            background-color:rgba(200,200,200,0.8);
            -webkit-transition: all 0.5s ease;
            -moz-transition: all 0.5s ease;
            -ms-transition: all 0.5s ease;
            -o-transition: all 0.5s ease;
            transition: all 0.5s ease;
            opacity:1;
			}
			#wrapper {
				position:relative;
				width:900px;
				height:900px;
			}

			#text {
				position:absolute;
				top:8px;
				left:530px;
				width:30px;
				height:50px;
				margin:auto auto auto auto;
				font-size:22px;
				color: #000000;
			}


			div.outerBorder {
				position:relative;
				top:400px;
				width:600px;
				height:44px;
				margin:auto auto auto auto;
				border:8px solid rgba(0,0,0,0.1);
				background: rgb(252,252,252); /* Old browsers */
				background: -moz-linear-gradient(top,  rgba(252,252,252,1) 0%, rgba(237,237,237,1) 100%); /* FF3.6+ */
				background: -webkit-gradient(linear, left top, left bottom, color-stop(0%,rgba(252,252,252,1)), color-stop(100%,rgba(237,237,237,1))); /* Chrome,Safari4+ */
				background: -webkit-linear-gradient(top,  rgba(252,252,252,1) 0%,rgba(237,237,237,1) 100%); /* Chrome10+,Safari5.1+ */
				background: -o-linear-gradient(top,  rgba(252,252,252,1) 0%,rgba(237,237,237,1) 100%); /* Opera 11.10+ */
				background: -ms-linear-gradient(top,  rgba(252,252,252,1) 0%,rgba(237,237,237,1) 100%); /* IE10+ */
				background: linear-gradient(to bottom,  rgba(252,252,252,1) 0%,rgba(237,237,237,1) 100%); /* W3C */
				filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#fcfcfc', endColorstr='#ededed',GradientType=0 ); /* IE6-9 */
				border-radius:72px;
				box-shadow: 0px 0px 10px rgba(0,0,0,0.2);
			}

			#border {
				position:absolute;
				top:10px;
				left:10px;
				width:500px;
				height:23px;
				margin:auto auto auto auto;
				box-shadow: 0px 0px 4px rgba(0,0,0,0.2);
				border-radius:10px;
			}

			#bar {
				position:absolute;
				top:0px;
				left:0px;
				width:20px;
				height:20px;
				margin:auto auto auto auto;
				border-radius:11px;
				border:2px solid rgba(30,30,30,0.05);
				background: rgb(0, 173, 246); /* Old browsers */
				box-shadow: 2px 0px 4px rgba(0,0,0,0.4);
			}
		</style>
		<script src="jquery-ui.js"></script>
		<script src="myjavascript.js"></script>
	</head>
	<body>
		<div id="mynetwork"></div>
		<div id="network_stats"></div>
		<button onclick="pause()">Start/Stop</button>
		<h1><br><br><br><br><br><br><br>Action log</h1>
		<div id="count_data"></div>
		<div id="return_data">Initializing...</div>
	</body>
</html>
