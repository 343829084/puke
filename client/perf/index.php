<html>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<head>

	<title>JavaScript CSV Draw</title>
</head>
<body>
<div id="content">
  <div id="indiv">
	<h1>A simple CSV Draw demo</h1>
	<textarea id="incsv"  rows="5" cols="30"></textarea>
        <button type="button" id="butt">转换</button>
  </div>
  <div id="outdiv">
  </div>
  <div id="graph"></div>

</div>


<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js" type="application/javascript"></script>
<script src="./js/Highcharts-2.2.4/highcharts.js" type="text/javascript"></script>
<script src="./js/Highcharts-2.2.4/highcharts.src.js" type="text/javascript"></script>
<script src="./js/Highcharts-2.2.4/highcharts-more.js" type="text/javascript"></script>
<script>

function showGraph()
{
    var chart;
        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'container',
                type: 'line',
                marginRight: 130,
                marginBottom: 25
            },
            title: {
                text: 'Monthly Average Temperature',
                x: -20 //center
            },
            subtitle: {
                text: 'Source: WorldClimate.com',
                x: -20
            },
            xAxis: {
                categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            },
            yAxis: {
                title: {
                    text: 'Temperature (°C)'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                formatter: function() {
                        return '<b>'+ this.series.name +'</b><br/>'+
                        this.x +': '+ this.y +'°C';
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'top',
                x: -10,
                y: 100,
                borderWidth: 0
            },
            series: [{
                name: 'Tokyo',
                data: [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]
            }, {
                name: 'New York',
                data: [-0.2, 0.8, 5.7, 11.3, 17.0, 22.0, 24.8, 24.1, 20.1, 14.1, 8.6, 2.5]
            }, {
                name: 'Berlin',
                data: [-0.9, 0.6, 3.5, 8.4, 13.5, 17.0, 18.6, 17.9, 14.3, 9.0, 3.9, 1.0]
            }, {
                name: 'London',
                data: [3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]
            }]
        });

}

function showCSV()
{
    var i, j, row, out = '',
	cell = '',
	csv = $('#incsv').val(), // get the input from the textbox
	arr = CSV.csvToArray(csv, true); // Convert the csv into an array

	// Each item in the array is a row from the csv
	// walk each row and create table cells for them
	for (i = 0; i < arr.length; i += 1) {
		row = arr[i];
		out += '<hr><br>';
		for (j = 0; j < row.length; j += 1) {
			cell = row[j];
			out += '<p>' + cell + '</p>';
		}
		out += '</br>';
	}

	// replace the current data with the new imported data
	$('#outdiv').html(out);

	showGraph();    
}

  
$(document).ready( function() {
    $('#butt').click(showCSV);
});
</script>
</body>
</html>
