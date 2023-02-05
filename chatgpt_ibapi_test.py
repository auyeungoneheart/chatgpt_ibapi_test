import ibapi
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order


class IBTrader(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.price = None

    def trade_options(self, symbol, expiry, strike, option_type, trade_type, quantity):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = "OPT"
        contract.lastTradeDateOrContractMonth = expiry
        contract.strike = strike
        contract.right = option_type
        contract.multiplier = "100"
        self.placeOrder(self.nextOrderId, contract, Order(orderType=trade_type, totalQuantity=quantity, action="SELL"))
        print("Options trade order placed for", symbol)

    def place_long_call_order(self, symbol, expiry, strike, quantity):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = "OPT"
        contract.lastTradeDateOrContractMonth = expiry
        contract.strike = strike
        contract.right = "CALL"
        contract.multiplier = "100"
        self.placeOrder(self.nextOrderId, contract, Order(orderType="BUY", totalQuantity=quantity, action="BUY"))
        print("Long call order placed for", symbol)

    def place_long_put_order(self, symbol, expiry, strike, quantity):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = "OPT"
        contract.lastTradeDateOrContractMonth = expiry
        contract.strike = strike
        contract.right = "PUT"
        contract.multiplier = "100"
        self.placeOrder(self.nextOrderId, contract, Order(orderType="BUY", totalQuantity=quantity, action="BUY"))
        print("Long put order placed for", symbol)

    def close_options_position(self, symbol, expiry, strike, option_type, trade_type, quantity):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = "OPT"
        contract.lastTradeDateOrContractMonth = expiry
        contract.strike = strike
        contract.right = option_type
        contract.multiplier = "100"
        self.placeOrder(self.nextOrderId, contract, Order(orderType=trade_type, totalQuantity=quantity, action="SELL"))
        print("Options position closed for", symbol)

    def tickPrice(self, tickerId, field, price, canAutoExecute):
        self.price = price
        if field == 4 and price >= 150:  # condition to place long call order: underlying price suddenly rises
            self.place_long_call_order("AAPL", "20230121", 145, 1)
            print("Long call order placed for AAPL")

        if field == 4 and price <= 50:  # condition to place long put order: underlying price suddenly falls
            self.place_long_put_order("AAPL", "20230121", 50, 1)
            print("Long put order placed for AAPL")

        if self.price * 2 <= 200:  # condition to close options position: options price doubles
            self.close_options_position("AAPL", "20230121", 145, "CALL", "SELL", 1)
            print("Options position closed for AAPL")


# Trade Apple options
ib_trader = IBTrader()
ib_trader.connect("127.0.0.1", 7497, clientId=1)
ib_trader.reqMarketDataType(4)
ib_trader.reqMktData(1, Contract(), "", False, False, [])

# Trade Tesla options
ib_trader.trade_options("TSLA", "20230121", 600, "CALL", "SELL", 1)

# Trade Microsoft options
ib_trader.trade_options("MSFT", "20230121", 250, "PUT", "SELL", 1)

# Start processing messages from IB API
ib_trader.run()
