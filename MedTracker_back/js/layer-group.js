var map = new ol.Map({
  layers: [
		new ol.layer.Tile({
      	source: new ol.source.MapQuest({layer: 'sat'})
    	}), new ol.layer.Group({
      layers: [
         new ol.layer.Tile({
         	source: new ol.source.TileWMS({
            	url: 'http://geoserver.compusult.net:8080/geoserver/SRTM_version4/wms',
					params:{
           			'LAYERS': 'SRTM_version4:SRTM'
					}
          	})
        }),
		  new ol.layer.Tile({
		  		source: new ol.source.TileWMS({
		  			url: 'http://peter-l.compusult.net:8080/geoserver/DTED2/wms',
		  			params:{
		  				'LAYERS': 'DTED2:dted2'
		 			}
		  		})
		  }),

        new ol.layer.Tile({
          source: new ol.source.TileJSON({
            url: 'http://api.tiles.mapbox.com/v3/' +
                'mapbox.world-borders-light.jsonp',
            crossOrigin: 'anonymous'
          })
        })
      ]
    })
  ],
  renderer: exampleNS.getRendererFromQueryString(),
  target: 'map',
  view: new ol.View({
    center: ol.proj.transform([37.40570, 8.81566], 'EPSG:4326', 'EPSG:3857'),
    zoom: 4
  })
});
            

function bindInputs(layerid, layer) {
  new ol.dom.Input($(layerid + ' .visible')[0])
      .bindTo('checked', layer, 'visible');
  $.each(['opacity', 'hue', 'saturation', 'contrast', 'brightness'],
      function(i, v) {
        new ol.dom.Input($(layerid + ' .' + v)[0])
            .bindTo('value', layer, v)
            .transform(parseFloat, String);
      }
  );
}

var mLayers

map.getLayers().forEach(function(layer, i) {
  bindInputs('#layer' + i, layer);
  if (layer instanceof ol.layer.Group) {
    layer.getLayers().forEach(function(sublayer, j) {
      bindInputs('#layer' + i + j, sublayer);
			if (j == '2') {
			}
    });
  }
});

$('#layertree li > span').click(function() {
  $(this).siblings('fieldset').toggle();
}).siblings('fieldset').hide();



var swipe = document.getElementById('swipe');

map.on('precompose', function(event) {
  var ctx = event.context;
  var width = ctx.canvas.width * (swipe.value / 100);

  ctx.save();
  ctx.beginPath();
  ctx.rect(width, 0, ctx.canvas.width - width, ctx.canvas.height);
  ctx.clip();
 });

map.on('postcompose', function(event) {
  var ctx = event.context;
  ctx.restore();
});

swipe.addEventListener('input', function() {
   map.render();
}, false);






