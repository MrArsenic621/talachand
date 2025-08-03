import os
import asyncio
import logging
from dotenv import load_dotenv
from telegram import Bot
from telegram.request import HTTPXRequest
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from price import get_all_vendors_prices

# === Load environment variables ===
load_dotenv()

# === Telegram Config ===
TELEGRAM_TOKEN = os.environ.get("TG_BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")  # "@yourchannel" or "-100..."

# === Proxy Setup ===
proxy_url = os.environ.get("PROXY_URL")  # e.g., "socks5://127.0.0.1:2334"

if proxy_url:
    request = HTTPXRequest(proxy=proxy_url)
    bot = Bot(token=TELEGRAM_TOKEN, request=request)
else:
    bot = Bot(token=TELEGRAM_TOKEN)


# === Logging ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# === Format the message ===
def format_prices(prices):
    def format_price(val):
        return f"{val:,}"

    header = "🟡 <b>قیمت طلای آبشده</b>\n\n"
    body = ""
    for item in prices:
        vendor = item["vendor"]
        buy = format_price(item["buy_price"])
        sell = format_price(item["sell_price"])
        body += f"🏷 <b>{vendor}</b>\n💰 خرید: {buy}  \n  🛒 فروش: {sell}\n\n"

    return header + body


# === Async Task ===
async def send_gold_prices():
    try:
        prices = get_all_vendors_prices()
        message = format_prices(prices)
        await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="HTML")
        logger.info("✅ Message sent successfully.")
    except Exception as e:
        logger.error(f"❌ Error sending message: {e}")


# === Main Runner ===
async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_gold_prices, "cron", minute="29,59")
    scheduler.start()

    await send_gold_prices()  # run once immediately

    while True:
        await asyncio.sleep(3600)  # Keep the loop alive


if __name__ == "__main__":
    asyncio.run(main())
