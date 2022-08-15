function getById(id) {
	return document.getElementById(id)
}


var parrentDiv = getById('candlestick-info-chart')
var chartDiv   = getById('trades-chart')
var priceOpen  = getById('price-open')
var quantity   = getById('quantity')

var symbol   = chartDiv.dataset.symbol
var minPrice = chartDiv.dataset.minprice

var chartWidth  = parrentDiv.offsetWidth
var chartHeight = chartWidth * 9 / 16

var gridLines       = '#f4f4f4'

var audio = new Audio('https://www.soundjay.com/misc/sounds/dream-harp-06.mp3')

// start websocket stream and update main div with current price
var url = `wss://stream.binance.com:9443/ws/${symbol}@trade`
var binanceSocket = new WebSocket(url)

binanceSocket.onmessage = (e) => {
  var obj = JSON.parse(e.data)
  var T = obj.T/1000
  var p = obj.p
  var q = obj.q

  lineSeries.update({time : T, value : p})
  minPriceLine.update({time : T, value : Number(minPrice)})

  priceOpen.innerHTML = p
  quantity.innerHTML  = q

  if (Number(p) > minPrice) {
		priceOpen.style.background = 'palegreen'
		//audio.play()
	} else {
		priceOpen.style.background = 'none'
	}

}


var chart = LightweightCharts.createChart(chartDiv, {
  width: chartWidth,
  height: chartHeight,

  rightPriceScale: {
		scaleMargins: {
			top: 0.1,
			bottom: 0.1,
		},
		borderColor: 'rgba(197, 203, 206, 0.4)',
	},

	timeScale: {
    timeVisible: true,
		borderColor: 'rgba(197, 203, 206, 0.4)',
	},

	grid: {
		vertLines: {
			color: 'rgba(197, 203, 206, 0.4)',
			style: LightweightCharts.LineStyle.Dotted,
		},
		horzLines: {
			color: 'rgba(197, 203, 206, 0.4)',
			style: LightweightCharts.LineStyle.Dotted,
		},
	},
  
   layout: {
    backgroundColor: '#ffffff',
    textColor: '#000',
  },
});

var lineSeries = chart.addAreaSeries({
  topColor: 'rgba(67, 83, 254, 0.7)',
  bottomColor: 'rgba(67, 83, 254, 0.1)',
  lineColor: 'rgba(67, 83, 254, 1)',
  lineWidth: 1,
});
lineSeries.setData([]);

var minPriceLine = chart.addLineSeries();
minPriceLine.setData([]);
