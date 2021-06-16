var chart = LightweightCharts.createChart(document.getElementById('chart'), {
    width: 600,
    height: 150,
    layout: {
        backgroundColor: '#000000',
        textColor: 'rgba(255, 255, 255, 0.9)',
    },
    grid: {
        vertLines: {
            color: 'rgba(197, 203, 206, 0.5)',
        },
        horzLines: {
            color: 'rgba(197, 203, 206, 0.5)',
        },
    },
    crosshair: {
        mode: LightweightCharts.CrosshairMode.Normal,
    },
    rightPriceScale: {
        borderColor: 'rgba(197, 203, 206, 0.8)',
    },
    timeScale: {
        borderColor: 'rgba(197, 203, 206, 0.8)',
    },
});

var candleSeries = chart.addCandlestickSeries({
    upColor: '#00ff00',
    downColor: '#ff0000',
    borderDownColor: '#ff0000',
    borderUpColor: '#00ff00',
    wickDownColor: 'rgba(255, 144, 0, 1)',
    wickUpColor: 'rgba(255, 144, 0, 1)',
});

fetch('http://localhost:5000/history')
    .then((r) => r.json())
    .then((response) => {
        console.log(response)

        candleSeries.setData(response);
})


//var select = document.getElementById('symbol_choosed');
//var text = select.options[select.selectedIndex].text;

var texto = $('#pair_choosed :selected').text();
var res = texto.toLowerCase();

var binanceSocket = new WebSocket("wss://stream.binance.com:9443/ws/"+res+"@kline_15m");
//var binanceSocket = new WebSocket("wss://stream.binance.com:9443/ws/bnbusdt@kline_15m");

binanceSocket.onmessage = function (event) {
    
    var message = JSON.parse(event.data);

    var candlestick = message.k;
    
    console.log(candlestick)

    candleSeries.update({
        //time: Date.now(),
        time: candlestick.t / 1000,
        open: candlestick.o,
        high: candlestick.h,
        low: candlestick.l,
        close: candlestick.c

    })
}