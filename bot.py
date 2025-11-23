import datetime as dt
from zoneinfo import ZoneInfo

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    Defaults,
)
BOT_TOKEN = "8506993035:AAEu2VEFhpquhGeSixAMObsTO82ZXH0_i14"

TZ_NAME = "Europe/Moscow"

MONTHS_RU = {
    1: "января",
    2: "февраля",
    3: "марта",
    4: "апреля",
    5: "мая",
    6: "июня",
    7: "июля",
    8: "августа",
    9: "сентября",
    10: "октября",
    11: "ноября",
    12: "декабря",
}


async def send_first_of_day(context: ContextTypes.DEFAULT_TYPE) -> None:
    now = dt.datetime.now(ZoneInfo(TZ_NAME))
    day = now.day
    month_name = MONTHS_RU[now.month]

    text = f"с первым {day} {month_name}"

    chat_id = context.job.chat_id
    await context.bot.send_message(chat_id=chat_id, text=text)

def get_days_to_new_year() -> int:
    now = dt.datetime.now(ZoneInfo(TZ_NAME))
    next_year = now.year + 1
    new_year_date = dt.datetime(next_year, 1, 1, tzinfo=ZoneInfo(TZ_NAME))

    delta = new_year_date - now
    return delta.days

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    job_queue = context.job_queue

    job_name = f"daily_first_{chat_id}"
    for job in job_queue.get_jobs_by_name(job_name):
        job.schedule_removal()
    job_queue.run_daily(
        send_first_of_day,
        time = dt.time(hour = 0, minute = 0),
        name = job_name,
        chat_id = chat_id,
    )

    days_left = get_days_to_new_year()

    await update.message.reply_text(
        f"Кстати, до Нового года осталось {days_left} дней!"
    )


def main() -> None:
    defaults = Defaults(tzinfo=ZoneInfo(TZ_NAME))

    application = Application.builder().token(BOT_TOKEN).defaults(defaults).build()
    application.add_handler(CommandHandler("start", start))

    application.run_polling()


if __name__ == "__main__":
    main()
