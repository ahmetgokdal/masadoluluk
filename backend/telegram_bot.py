"""
Telegram bot integration for sending reports
"""
import os
import logging
from telegram import Bot
from telegram.error import TelegramError
from pathlib import Path

logger = logging.getLogger(__name__)

async def send_telegram_message(bot_token: str, chat_id: str, message: str):
    """Send text message via Telegram"""
    try:
        bot = Bot(token=bot_token)
        await bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
        return True
    except TelegramError as e:
        logger.error(f"Telegram error: {e}")
        return False
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return False

async def send_telegram_document(bot_token: str, chat_id: str, file_path: str, caption: str = None):
    """Send document/file via Telegram"""
    try:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return False
        
        bot = Bot(token=bot_token)
        with open(file_path, 'rb') as file:
            await bot.send_document(
                chat_id=chat_id,
                document=file,
                caption=caption,
                parse_mode='Markdown'
            )
        return True
    except TelegramError as e:
        logger.error(f"Telegram error: {e}")
        return False
    except Exception as e:
        logger.error(f"Error sending document: {e}")
        return False

async def send_report_to_parent(bot_token: str, chat_id: str, cabin_no: int, student_name: str, report_data: dict):
    """Send formatted report to parent's Telegram"""
    try:
        message = f"""
📊 *Kabin {cabin_no} - {student_name} Raporu*

📅 Tarih: {report_data.get('date', 'N/A')}
⏱️ Toplam Süre: {report_data.get('total_hours', 0):.1f} saat
📈 Oturum Sayısı: {report_data.get('sessions_count', 0)}

✅ Sistem tarafından otomatik oluşturulmuştur.
        """
        
        return await send_telegram_message(bot_token, chat_id, message.strip())
    except Exception as e:
        logger.error(f"Error sending report: {e}")
        return False

async def send_alert_to_parent(bot_token: str, chat_id: str, cabin_no: int, student_name: str, alert_message: str):
    """Send alert to parent's Telegram"""
    try:
        message = f"""
⚠️ *Uyarı - Kabin {cabin_no}*

👤 Öğrenci: {student_name}
📝 {alert_message}

🕐 Zaman: {Path(__file__).name}
        """
        
        return await send_telegram_message(bot_token, chat_id, message.strip())
    except Exception as e:
        logger.error(f"Error sending alert: {e}")
        return False
