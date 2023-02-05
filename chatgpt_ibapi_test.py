import ibapi
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
import logging

class IBWrapper(EWrapper):
    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        print("Error. Id:", reqId, " Code:", errorCode, " Msg:", errorString)

    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float, attrib: TickAttrib):
        if reqId == 1: # Apple
            if price > 150.00: # replace the order with a call option if the stock price rises above 150.00
                self.placeOrder(reqId, contract1, order1)
            elif price < 140.00: # replace the order with a put option if the stock price drops below 140.00
                contract1.right = "P" # "C" for call options, "P" for put options
                self.placeOrder(reqId, contract1, order1)
            print("Tick Price for Apple. Ticker Id:", reqId, "tickType:", tickType, "Price:", price, "CanAutoExecute:", attrib.canAutoExecute)
        elif reqId == 2: # Tesla
            if price > 700.00: # replace the order with a call option if the stock price rises above 700.00
                self.placeOrder(reqId, contract2, order2)
            elif price < 650.00: # replace the order with a put option if the stock price drops below 650.00
                contract2.right = "P" # "C" for call options, "P" for put options
                self.placeOrder(reqId, contract2, order2)
            print("Tick Price for Tesla. Ticker Id:", reqId, "tickType:", tickType, "Price:", price, "CanAutoExecute:", attrib.canAutoExecute)
        elif reqId == 3: # Microsoft
            if price > 140.00: # replace the order with a call option if the stock price rises above 140.00
                self.placeOrder(reqId, contract3, order3)
            elif price < 130.00: # replace the order with a put option if the stock price drops below 130.00
                contract3.right = "P" # "C" for call options, "P" for put options
                self.placeOrder(reqId, contract3, order3)
            print("Tick Price for Microsoft. Ticker Id:", reqId, "tickType:", tickType, "Price:", price, "CanAutoExecute:", attrib.canAutoExecute)

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        if status == "Filled":
            logging.basicConfig(filename="order_filled.log", level=logging.INFO)
            logging.info("Order filled. Order Id: {}".format(orderId))

class IBClient(EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def run(self):
        self.connect("127.0.0.1", 7496, clientId=0)
        self.reqMarketDataType(MarketDataType.DELAYED)

        # Define contracts for Apple, Tesla, and Microsoft
        contract1 = Contract()
        contract1.symbol = "AAPL"
        contract1.secType = "OPT"
        contract1.exchange = "SMART"
        contract1.currency = "USD"
        contract1.right = "C"  # "C" for call options, "P" for put options
        contract1.strike = 145.00
        contract1.multiplier = 100
        contract1.expiry = "2023-06-17"

        contract2 = Contract()
        contract2.symbol = "TSLA"
        contract2.secType = "OPT"
        contract2.exchange = "SMART"
        contract2.currency = "USD"
        contract2.right = "C"  # "C" for call options, "P" for put options
        contract2.strike = 680.00
        contract2.multiplier = 100
        contract2.expiry = "2023-06-17"

        contract3 = Contract()
        contract3.symbol = "MSFT"
        contract3.secType = "OPT"
        contract3.exchange = "SMART"
        contract3.currency = "USD"
        contract3.right = "C"  # "C" for call options, "P" for put options
        contract3.strike = 135.00
        contract3.multiplier = 100
        contract3.expiry = "2023-06-17"

        # Define orders for Apple, Tesla, and Microsoft
        order1 = Order()
        order1.action = "BUY"
        order1.orderType = "LMT"
        order1.totalQuantity = 1
        order1.lmtPrice = 0.50

        order2 = Order()
        order2.action = "BUY"
        order2.orderType = "LMT"
        order2.totalQuantity = 1
        order2.lmtPrice = 0.50

        order3 = Order()
        order3.action = "BUY"
        order3.orderType = "LMT"
        order3.totalQuantity = 1
        order3.lmtPrice = 0.50

        # Request market data for Apple, Tesla, and Microsoft
        self.reqMktData(1, contract1, "", False, False, [])
        self.reqMktData(2, contract2, "", False, False, [])
        self.reqMktData(3, contract3, "", False, False, [])

        self.run()


if __name__ == "__main__":
    app = IBClient()
    app.run()
