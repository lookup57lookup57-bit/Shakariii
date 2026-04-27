import asyncio
import random
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

router = Router()

ALLOWED_GROUP = -1003459867774
OWNER_ID = 8315528188

# ========== ASCII LOADING BAR ==========
class StartLoader:
    """Loading bar animation untuk /start command"""
    
    @staticmethod
    async def loading_bar(message: Message, text: str = "Starting..."):
        """Loading bar 10% → 100% dengan ASCII"""
        # Progress bar stages
        bars = [
            "[■□□□□□□□□□] 10%",
            "[■■□□□□□□□□] 20%",
            "[■■■□□□□□□□] 30%",
            "[■■■■□□□□□□] 40%",
            "[■■■■■□□□□□] 50%",
            "[■■■■■■□□□□] 60%",
            "[■■■■■■■□□□] 70%",
            "[■■■■■■■■□□] 80%",
            "[■■■■■■■■■□] 90%",
            "[■■■■■■■■■■] 100%"
        ]
        
        # ASCII spinners
        spinners = ["|", "/", "-", "\\", "+", "x", "*", "#"]
        
        # ASCII art ZACATECAS
        zacatecas_art = [
            "╔════════════════════╗",
            "║  ZACATECAS HITTER  ║",
            "╚════════════════════╝"
        ]
        
        # Start dengan animasi
        loading_msg = await message.answer(
            f"{zacatecas_art[0]}\n"
            f"{zacatecas_art[1]}\n"
            f"{zacatecas_art[2]}\n\n"
            f"{spinners[0]} {text}\n"
            f"`{bars[0]}`",
            parse_mode=ParseMode.HTML
        )
        
        # Animasi spinner dulu
        for i in range(6):
            try:
                spinner = spinners[i % len(spinners)]
                await loading_msg.edit_text(
                    f"{zacatecas_art[0]}\n"
                    f"{zacatecas_art[1]}\n"
                    f"{zacatecas_art[2]}\n\n"
                    f"{spinner} {text}\n"
                    f"`{bars[0]}`",
                    parse_mode=ParseMode.HTML
                )
                await asyncio.sleep(0.15)
            except:
                break
        
        # Progress bar naik 10% → 100%
        for i, bar in enumerate(bars):
            try:
                spinner = random.choice(spinners)
                percent = (i + 1) * 10
                
                # ASCII art yang berubah
                if percent <= 30:
                    art_line = "╔════════════════════╗"
                elif percent <= 60:
                    art_line = "║  ■■■□□□□□□□□□□□□  ║"
                elif percent <= 90:
                    art_line = "║  ■■■■■■■■□□□□□□□  ║"
                else:
                    art_line = "║  ■■■■■■■■■■■■■■■  ║"
                
                await loading_msg.edit_text(
                    f"{zacatecas_art[0]}\n"
                    f"{art_line}\n"
                    f"{zacatecas_art[2]}\n\n"
                    f"{spinner} {text}\n"
                    f"`{bar}`",
                    parse_mode=ParseMode.HTML
                )
                await asyncio.sleep(0.2)
            except:
                continue
        
        # Final check mark
        try:
            await loading_msg.edit_text(
                f"{zacatecas_art[0]}\n"
                f"║  ✓ READY TO HIT  ║\n"
                f"{zacatecas_art[2]}\n\n"
                f"✓ {text}\n"
                f"`{bars[-1]}`",
                parse_mode=ParseMode.HTML
            )
        except:
            pass
        
        await asyncio.sleep(0.5)
        return loading_msg

def check_access(msg: Message) -> bool:
    if msg.chat.id == ALLOWED_GROUP:
        return True
    if msg.chat.type == "private" and msg.from_user.id == OWNER_ID:
        return True
    return False

@router.message(Command("start"))
async def start_handler(msg: Message):
    if not check_access(msg):
        await msg.answer(
            "<blockquote><code>ZACATECAS HITTER - ACCESS DENIED</code></blockquote>\n\n"
            "<blockquote>「🔪」 Contact : <code>@ile_gal</code></blockquote>",
            parse_mode=ParseMode.HTML
        )
        return
    
    # SHOW LOADING BAR ANIMATION
    loading = await StartLoader.loading_bar(msg, "Initializing ZACATECAS HITTER...")
    
    # Setelah loading selesai, tampilkan menu
    welcome = (
        "<blockquote><code>╔════════════════════╗</code>\n"
        "<code>║  ZACATECAS HITTER  ║</code>\n"
        "<code>╚════════════════════╝</code></blockquote>\n\n"
        "<blockquote>「🔪」 <code>Stripe Checkout Charger</code>\n"
        "「⚡」 <code>Premium Proxy System</code>\n"
        "「💎」 <code>Card Testing Tools</code></blockquote>\n\n"
        "<blockquote>「🎯」 <b>MAIN COMMANDS</b></blockquote>\n"
        "<blockquote>    • <code>/co url</code> - Parse Stripe checkout\n"
        "    • <code>/co url cards</code> - Charge cards\n"
        "    • <code>/addproxy proxy</code> - Add proxy\n"
        "    • <code>/proxy check</code> - Check proxies</blockquote>\n\n"
        "<blockquote>「💳」 <b>CARD FORMAT</b></blockquote>\n"
        "<blockquote>    • <code>cc|mm|yy|cvv</code>\n"
        "    • <code>4242424242424242|12|25|123</code></blockquote>\n\n"
        "<blockquote>「🔧」 <b>PREMIUM SYSTEM</b></blockquote>\n"
        "<blockquote>    • <code>/redeem CODE</code>\n"
        "    • <code>/zacatecas</code> - Full menu</blockquote>\n\n"
        "<blockquote>「📞」 <b>CONTACT</b></blockquote>\n"
        "<blockquote>    • <code>@ile_gal</code>\n"
        "    • <code>ZACATECAS HITTER v2.0</code></blockquote>"
    )
    
    await loading.edit_text(welcome, parse_mode=ParseMode.HTML)

@router.message(Command("help"))
async def help_handler(msg: Message):
    if not check_access(msg):
        await msg.answer(
            "<blockquote><code>ZACATECAS HITTER - ACCESS DENIED</code></blockquote>\n\n"
            "<blockquote>「🔪」 Contact : <code>@ile_gal</code></blockquote>",
            parse_mode=ParseMode.HTML
        )
        return
    
    # LOADING BAR untuk help juga
    loading = await StartLoader.loading_bar(msg, "Loading help menu...")
    
    help_text = (
        "<blockquote><code>╔════════════════════╗</code>\n"
        "<code>║  ZACATECAS HITTER  ║</code>\n"
        "<code>╚════════════════════╝</code></blockquote>\n\n"
        "<blockquote>「📋」 <b>ALL COMMANDS</b></blockquote>\n"
        "<blockquote>「🔪」 <code>/start</code> - Show welcome\n"
        "「🎯」 <code>/help</code> - Show this help\n"
        "「⚡」 <code>/co url</code> - Parse checkout\n"
        "「💳」 <code>/co url cards</code> - Charge cards</blockquote>\n\n"
        "<blockquote>「🔧」 <b>PROXY COMMANDS</b></blockquote>\n"
        "<blockquote>    • <code>/addproxy proxy</code>\n"
        "    • <code>/removeproxy proxy</code>\n"
        "    • <code>/removeproxy all</code>\n"
        "    • <code>/proxy check</code></blockquote>\n\n"
        "<blockquote>「💎」 <b>PREMIUM COMMANDS</b></blockquote>\n"
        "<blockquote>    • <code>/redeem CODE</code>\n"
        "    • <code>/gencode 1d 10</code> (admin)\n"
        "    • <code>/codes</code> (admin)\n"
        "    • <code>/delcode CODE</code> (admin)\n"
        "    • <code>/zacatecas</code> - Full menu</blockquote>\n\n"
        "<blockquote>「🔗」 <b>SUPPORTED URLS</b></blockquote>\n"
        "<blockquote>    • <code>checkout.stripe.com</code>\n"
        "    • <code>buy.stripe.com</code></blockquote>\n\n"
        "<blockquote>「📞」 <code>Contact: @ile_gal</code></blockquote>"
    )
    
    await loading.edit_text(help_text, parse_mode=ParseMode.HTML)

@router.message(Command("menu"))
async def menu_handler(msg: Message):
    """Alternative menu command"""
    if not check_access(msg):
        await msg.answer(
            "<blockquote><code>ZACATECAS HITTER - ACCESS DENIED</code></blockquote>\n\n"
            "<blockquote>「🔪」 Contact : <code>@ile_gal</code></blockquote>",
            parse_mode=ParseMode.HTML
        )
        return
    
    # Quick loading untuk menu
    loading = await StartLoader.loading_bar(msg, "Loading menu...")
    
    menu_text = (
        "<blockquote><code>╔════════════════════╗</code>\n"
        "<code>║  ZACATECAS MENU   ║</code>\n"
        "<code>╚════════════════════╝</code></blockquote>\n\n"
        "<blockquote>「⚡」 <code>QUICK START</code></blockquote>\n"
        "<blockquote>1. Add proxy: <code>/addproxy host:port:user:pass</code>\n"
        "2. Parse checkout: <code>/co https://checkout.stripe.com/...</code>\n"
        "3. Charge cards: <code>/co url 4242424242424242|12|25|123</code></blockquote>\n\n"
        "<blockquote>「🔧」 <code>NEED HELP?</code></blockquote>\n"
        "<blockquote>• <code>/help</code> - All commands\n"
        "• <code>/zacatecas</code> - Full features\n"
        "• Contact: <code>@ile_gal</code></blockquote>\n\n"
        "<blockquote>「💎」 <code>STATUS: ONLINE ✓</code></blockquote>"
    )
    
    await loading.edit_text(menu_text, parse_mode=ParseMode.HTML)