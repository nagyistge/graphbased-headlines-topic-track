var count = 0;
var maxCount = 5000;
var maxChartData = 40;
var interval = 5000;
var processing = false;
var timePoint = 0;
var elapsed = 0;
var _Sec = 1;
var _USec = 0;
var ssName = "";
var oldName = "";
var cancel = false;

// Blank Data
var data  = {};

//Option for graph
var locales = {
  en: {
    edit: 'Edit',
    del: 'Delete selected',
    back: 'Back',
    addNode: 'Add Node',
    addEdge: 'Add Edge',
    editNode: 'Edit Node',
    editEdge: 'Edit Edge',
    addDescription: 'Click in an empty space to place a new node.',
    edgeDescription: 'Click on a node and drag the edge to another node to connect them.',
    editEdgeDescription: 'Click on the control points and drag them to a node to connect to it.',
    createEdgeError: 'Cannot link edges to a cluster.',
    deleteClusterError: 'Clusters cannot be deleted.',
    editClusterError: 'Clusters cannot be edited.'
  }
}
var options = {
	autoResize: true,
	height: '100%',
	width: '100%',
	locale: 'en',
	locales: locales,
	clickToUse: false,
	physics: true,
    configure:function (option, path) {
      if (path.indexOf('smooth') !== -1 || option === 'smooth') {
        return true;
      }
      return false;
    },
	nodes: {
		shape: 'dot',
		font: {
                size: 28,
                color: '#ffffff'
            },
        scaling:{
            label: {
              min:8,
              max:20
            }
        }
    },
    edges: {
     // smooth: {
     //   type: 'continuous'
     // }
		color: {inherit: 'both'},
		smooth: false
    }
};
	

$(document).ready(function() {
	// This will get the first returned node in the jQuery collection.
	var container = document.getElementById("mynetwork");
	var nodes = new vis.DataSet([
	]);

  // create an array with edges
	var edges = new vis.DataSet([
	]);
	
	data = {
    nodes: nodes,
    edges: edges
	};
	// Network options


	var network = new vis.Network(container, data, options);
	network.on("stabilizationProgress", function(params) {
                var maxWidth = 496;
                var minWidth = 20;
                var widthFactor = params.iterations/params.total;
                var width = Math.max(minWidth,maxWidth * widthFactor);

                document.getElementById('bar').style.width = width + 'px';
                document.getElementById('text').innerHTML = Math.round(widthFactor*100) + '%';
            });
    network.once("stabilizationIterationsDone", function() {
                document.getElementById('text').innerHTML = '100%';
                document.getElementById('bar').style.width = '496px';
                document.getElementById('loadingBar').style.opacity = 0;
                // really clean the dom element
                setTimeout(function () {document.getElementById('loadingBar').style.display = 'none';}, 500);
            });
	window.onresize = function() {network.fit();}
	process();
	
});

function process() {
	if (cancel) return;
	if (processing) {
		setTimeout(process, interval);
		return;
	}
	else {
		
		processing = true;
		ssName = "";
		oldName = "";
	
		$.ajax({
		   method: "POST",
		   url: "getMongoDB.php",
		   data: { lastSec : _Sec, lastUSec : _USec }
		})
		.done(function( json_data ) {
			if (count > 0) $("#count_data").text(count);
			var msg = jQuery.parseJSON(json_data);
			var content = "";
			var datatxt = "";
			var timetxt = "";
			var innerCount=0;
			$.each( msg, function( i, row ) {
				innerCount = innerCount + 1;
				timetxt = "<i>" + innerCount + "</i>. [Sec= " + row["timeSec"]  + ". USecs: " +  row["timeUSec"] + "] : ";
				if (_Sec < row["timeSec"]) {
				   _Sec = row["timeSec"];
				   _USec = row["timeUSec"];
				}
				else if (_Sec == row["timeSec"] && _USec < row["timeUSec"]) {
				   _USec = row["timeUSec"];
				} 	
				
				datatxt = "<b>" + row["nodes"] + "</b> || '"+ row["edges"] + "'";
				content += "<div>" + timetxt + datatxt + "</div> <br>";
				$("#return_data").html(content);
				
				// Now play with the data. Kakakak
				try {
					// Start with nodes
					var node_srt = row["nodes"].substring(2, row["nodes"].length-2);
					var node_list = node_srt.split("\", \"");	// Get list of new nodes WITH FREQ included
					var node_list_ids = []; // List of new node IDs (word)
					var edge_srt = row["edges"].substring(2, row["edges"].length-2);
					var edge_list = edge_srt.split("\", \"");	// Get list of new edges
					var edge_list_ids = []; // List of new edge IDs (word)
					var nd;
					var ed;
					var report = '';
					
					// Compute list of Node Id and list ID
					for (nd in node_list) {
						res = node_list[nd].split(":");
						//alert(res);
						if (res.length == 2)
							node_list_ids.push(res[0]);
					}
					
					for (ed in edge_list) {
						res = edge_list[ed].split(":");
						if (res.length == 2)
							edge_list_ids.push(res[0]);
					}
					
					// Delete edges are longer in graph
					var toeliItems=[];
					var current_edges = data.edges.get();
					for (ed in current_edges){
						//alert(current_edges[ed].id + "XxX" + !(edge_list.indexOf(current_edges[ed].id) >= 0) +"XxX"+ edge_list);
						// get to the left of ':' 
						idstr = current_edges[ed].id;
						//idstr = idstr.substring(0, idstr.indexOf(":"));
						if (!(edge_list_ids.indexOf(idstr) >= 0)){
							toeliItems.push(idstr);
						}
					}
					report = report + '\n - FOUND ' + toeliItems.length + ' old edges:' + toeliItems;
					var count_1 = 0;
					for (ed in toeliItems) {
						var rms = data.edges.remove(toeliItems[ed]);
						if (rms.length==1) count_1 = count_1 + 1;
					}
					report = report + '\n - DELETED ' + count_1 + ' old edges';
					
					// Delete nodes are longer in graph
					toeliItems=[];
					var current_nodes = data.nodes.get();
					for (nd in current_nodes){
						idstr = current_nodes[nd].id;
						//idstr = idstr.substring(0, idstr.indexOf(":"));
						if (!(node_list_ids.indexOf(idstr) >= 0)){
							toeliItems.push(idstr);
						}
					}
					report = report + '\n - FOUND ' + toeliItems.length + ' old nodes';
					//alert(toeliItems.length);
					count_1 = 0;
					for (nd in toeliItems) {
						var rms = data.nodes.remove(toeliItems[nd]);
						if (rms.length==1) count_1 = count_1 + 1;
					}
					report = report + '\n - DELETED ' + count_1 + ' old nodes';
					
					// Add new nodes
					count_1	=0;	
					var count_2	=0;						
					for (nd in node_list) {
						res = node_list[nd].split(":");
						//alert(res);
						if (res.length == 2)
							if (data.nodes.get(res[0]) == null) {// Node is not exist
								data.nodes.add({id: res[0],  value: Number(res[1]), label: res[0] , title: 'frequency:' + res[1], group: Number(res[1])});
								count_1 = count_1 + 1;
							}
							else {
								data.nodes.update({id: res[0], title: 'frequency:' + res[1], group: Number(res[1])});
								count_2 = count_2 + 1;
							}
					}
					report = report + '\n - Added ' + count_1 + ' and updated ' + count_2 + 'nodes out of ' + node_list.length;
				
					// Add new edges
					count_1	=0;
					count_2	=0;	
					for (ed in edge_list) {
						res = edge_list[ed].split(" ");
						if (res.length == 2)
							// Split the second element to get freq
							res2 = res[1].split(":");
							if (res2.length == 2)
								if (data.edges.get(res[0] + ' ' +res2[0]) == null){ // edge is not exist
									data.edges.add({id: (res[0] + ' ' +res2[0]), from: res[0], to: res2[0], value: Number(res2[1]), title: 'frequency:' + res2[1], group: Number(res2[1])});
									count_1 = count_1 + 1;
								}
								else {
									data.edges.update({id: (res[0] + ' ' +res2[0]), title: 'frequency:' + res2[1], group: Number(res2[1])});
									count_2 = count_2 + 1;
								}
							
					}
					report = report + '\n - Added ' + count_1 + ' and updated ' + count_2 + 'edges out of ' + edge_list.length;
					// Post processing checked
					
					current_edges = data.edges.get();
					current_nodes = data.nodes.get();
					//Report by alert
					//alert('Inconsisten in node number!' + node_srt.length + ' ' + node_list.length + ' ' + current_nodes.length + '\n' + 'Inconsisten in edge number!' + edge_srt.length + ' ' + edge_list.length + ' ' + current_edges.length + report);
					
					
				}
				catch(err) {
					alert(err.message);
				}
				
				$("#network_stats").html("Num. of node:" + data.nodes.length + ". Num. of edge:" + data.edges.length);
			
			});
			
			if (count > 0) {
				
				// Update sensor data
			//$("#return_data").html(innerCount);
			//	data.nodes.add({id: count, label: count});
			}
			processing = false;
			count++;
		});
		
		if (count < maxCount) {
			setTimeout(process, interval);
		}
	}
}

function pause() {
	if (!cancel) {
		cancel = true;
	}
	else {
		cancel = false;
		elapsed = 0;
		process();
	}
}

function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min)) + min;
}

jQuery.fn.removeAttributes = function() {
  return this.each(function() {
    var attributes = $.map(this.attributes, function(item) {
      return item.name;
    });
    var img = $(this);
    $.each(attributes, function(i, item) {
    img.removeAttr(item);
    });
  });
}

var resizeTimer;
$(window).resize(function() {
    network.fit();
});
