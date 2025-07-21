import blpapi
from blpapi import SessionOptions, Session
from datetime import datetime
import time

def fetch_bloomberg_data(tickers):
    session_options = SessionOptions()
    session_options.setServerHost('localhost')  # Default Bloomberg host
    session_options.setServerPort(8194)         # Default Bloomberg port

    session = Session(session_options)
    if not session.start():
        print("Failed to start Bloomberg session.")
        return

    if not session.openService("//blp/refdata"):
        print("Failed to open //blp/refdata service.")
        return

    ref_data_service = session.getService("//blp/refdata")
    request = ref_data_service.createRequest("ReferenceDataRequest")
    
    for ticker in tickers:
        request.append("securities", ticker)

    request.append("fields", "PX_LAST")         # Last traded price
    request.append("fields", "PX_CLOSE_1D")     # Previous close

    session.sendRequest(request)

    results = {}
    while True:
        ev = session.nextEvent(500)
        for msg in ev:
            if msg.messageType() == "ReferenceDataResponse":
                for security_data in msg.getElement("securityData").values():
                    ticker = security_data.getElementAsString("security")
                    field_data = security_data.getElement("fieldData")

                    px_last = field_data.getElementAsFloat("PX_LAST")
                    px_close = field_data.getElementAsFloat("PX_CLOSE_1D")
                    change = px_last - px_close
                    percent = (change / px_close) * 100 if px_close != 0 else 0

                    results[ticker] = {
                        "last_price": px_last,
                        "previous_close": px_close,
                        "change": change,
                        "percent_change": percent
                    }

        if ev.eventType() == blpapi.Event.RESPONSE:
            break

    return results

def display_results(results):
    print(f"Bloomberg Stock Tracker ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")
    for ticker, data in results.items():
        print(f"   {ticker}")
        print(f"   Current Price     : ${data['last_price']:.2f}")
        print(f"   Previous Close    : ${data['previous_close']:.2f}")
        print(f"   Change            : ${data['change']:.2f} ({data['percent_change']:.2f}%)\n")

if __name__ == "__main__":
    tickers = ["NVDA US Equity", "AMD US Equity"]
    stock_data = fetch_bloomberg_data(tickers)
    display_results(stock_data)