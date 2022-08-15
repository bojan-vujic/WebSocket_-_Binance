function getById(id) {
	return document.getElementById(id)
}

var parrentDiv = getById('candlestick-info-chart')
var chartDiv   = getById('candlestick-chart')
var priceOpen  = getById('price-open')
var priceHigh  = getById('price-high')
var priceLow   = getById('price-low')
var priceClose = getById('price-close')
var btn        = getById('monitor-price')

var indexOfMinPrice = 0;
var gridLines       = '#f4f4f4'
var chartWidth      = parrentDiv.offsetWidth
var chartHeight     = chartWidth * 9 / 16

var symbol   = chartDiv.dataset.symbol
var interval = chartDiv.dataset.interval
var minPrice = chartDiv.dataset.minprice
var data     = JSON.parse(chartDiv.dataset.dataarray)
var dataMin  = JSON.parse(chartDiv.dataset.dataminarray)
console.log(dataMin)


var audio = new Audio('https://www.soundjay.com/misc/sounds/dream-harp-06.mp3')


var url = `wss://stream.binance.com:9443/ws/${symbol}@kline_${interval}`
var binanceSocket = new WebSocket(url)

binanceSocket.onmessage = (e) => {
	var obj = JSON.parse(e.data)
	var t, o, h, l, c
	t = obj.k.t/1000, 
	o = obj.k.o
	h = obj.k.h
	l = obj.k.l
	c = obj.k.c
	
	series.update({time : t, open : o, high : h, close : c})
	minPriceLine.update({time : t, value : minPrice})
	
	priceOpen.innerHTML  = o
	priceHigh.innerHTML  = h
	priceLow.innerHTML   = l
	priceClose.innerHTML = c
	if (Number(c) > minPrice) {
		priceClose.style.background = 'palegreen'
		//audio.play()
	} else {
		priceClose.style.background = 'none'
	}
}


var chart = LightweightCharts.createChart(chartDiv, {
  width: chartWidth,
  height: chartHeight,
	timeScale: {
		timeVisible: true,
    borderColor: '#D1D4DC',
		},
  rightPriceScale: {
  	borderColor: '#D1D4DC',
  },
   layout: {
    backgroundColor: '#ffffff',
    textColor: '#000',
  },
  grid: {
    horzLines: {
      color: gridLines,
    },
    vertLines: {
      color: gridLines,
    },
  },
});


var minPriceLine = chart.addLineSeries();
minPriceLine.setData(dataMin);

var series = chart.addCandlestickSeries({
		upColor: 'rgb(38,166,154)',
		downColor: 'rgb(255,82,82)',
		wickUpColor: 'rgb(38,166,154)',
		wickDownColor: 'rgb(255,82,82)',
		borderVisible: true,
  });


series.setData(data);


chart.timeScale().applyOptions({ fixLeftEdge: true })



