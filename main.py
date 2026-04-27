#!/usr/bin/env python3
"""
ZACATECAS AUTO HITTER
"""

import asyncio
import gc
import logging
import os
import signal
import sys
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import BOT_TOKEN
from commands import router

# ========== ZACATECAS LOGO WARNA MERAH & BIRU ==========
ZACATECAS_LOGO = """
\033[1;31m███████╗ █████╗  ██████╗ █████╗ ████████╗███████╗ █████╗\033[0m
\033[1;31m╚══███╔╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔════╝██╔══██╗\033[0m
\033[1;31m  ██╔╝ ███████║██║     ███████║   ██║   █████╗  ███████║\033[0m
\033[1;31m ██╔╝  ██╔══██║██║     ██╔══██║   ██║   ██╔══╝  ██╔══██║\033[0m
\033[1;31m███████╗██║  ██║╚██████╗██║  ██║   ██║   ███████╗██║  ██║\033[0m
\033[1;31m╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝\033[0m
\033[1;34m    █████╗ ██╗   ██╗████████╗ ██████╗\033[0m                
\033[1;34m   ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗\033[0m               
\033[1;34m   ███████║██║   ██║   ██║   ██║   ██║\033[0m               
\033[1;34m   ██╔══██║██║   ██║   ██║   ██║   ██║\033[0m               
\033[1;34m   ██║  ██║╚██████╔╝   ██║   ╚██████╔╝\033[0m               
\033[1;34m   ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝\033[0m                
\033[1;35m            BY @ile_gal\033[0m
"""

# ========== SETUP LOGGING ==========
def setup_logging():
    """Setup logging configuration"""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f"zacatecas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file, encoding='utf-8')
        ]
    )
    
    return logging.getLogger(__name__)

logger = setup_logging()

# ========== MEMORY MANAGEMENT ==========
class MemoryManager:
    """Manage memory usage to prevent crashes"""
    
    @staticmethod
    def setup_limits():
        """Set memory limits if available"""
        try:
            import resource
            # 256MB soft limit, 512MB hard limit
            soft = 256 * 1024 * 1024  # 256MB
            hard = 512 * 1024 * 1024  # 512MB
            resource.setrlimit(resource.RLIMIT_AS, (soft, hard))
            logger.info(f"Memory limits set: {soft//1024//1024}MB/{hard//1024//1024}MB")
        except Exception as e:
            logger.warning(f"Could not set memory limits: {e}")
    
    @staticmethod
    def cleanup():
        """Force garbage collection"""
        collected = gc.collect(generation=2)
        logger.debug(f"Garbage collected: {collected} objects")
    
    @staticmethod
    def get_memory_usage():
        """Get current memory usage in MB"""
        try:
            import psutil
            process = psutil.Process(os.getpid())
            return process.memory_info().rss / 1024 / 1024
        except ImportError:
            return 0

# ========== BOT MANAGER ==========
class ZacatecasBot:
    """Main bot manager with auto-restart capability"""
    
    def __init__(self):
        self.bot = None
        self.dp = None
        self.start_time = None
        self.is_running = False
        self.restart_count = 0
        self.max_restarts = 5
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum}, initiating shutdown...")
        self.is_running = False
    
    def _print_banner(self):
        """Print startup banner with colors"""
        print("\n" + ZACATECAS_LOGO)
        print("\033[1;36m" + "=" * 60 + "\033[0m")
        print("\033[1;33m🚀 ZACATECAS AUTO HITTER INITIALIZING...\033[0m")
        print("\033[1;36m" + "=" * 60 + "\033[0m")
        print(f"\033[1;32mStart Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\033[0m")
        print(f"\033[1;32mPID: {os.getpid()}\033[0m")
        print("\033[1;36m" + "=" * 60 + "\033[0m\n")
    
    async def initialize(self):
        """Initialize bot components"""
        try:
            # Print banner
            self._print_banner()
            
            # Setup memory limits
            MemoryManager.setup_limits()
            
            # Create bot instance
            self.bot = Bot(
                token=BOT_TOKEN,
                default=DefaultBotProperties(
                    parse_mode=ParseMode.HTML,
                    link_preview_is_disabled=True,
                    allow_sending_without_reply=True
                )
            )
            
            # Create dispatcher
            self.dp = Dispatcher()
            
            # Include router
            self.dp.include_router(router)
            
            # Register error handler
            self.dp.errors.register(self._error_handler)
            
            self.start_time = datetime.now()
            self.restart_count += 1
            
            logger.info(f"✅ Bot initialized successfully (Restart #{self.restart_count})")
            logger.info(f"📊 Memory usage: {MemoryManager.get_memory_usage():.2f} MB")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize bot: {e}")
            return False
    
    async def _error_handler(self, update, exception):
        """Global error handler"""
        logger.error(f"Error in update {update}: {exception}", exc_info=True)
        return True
    
    async def _periodic_maintenance(self):
        """Run periodic maintenance tasks"""
        while self.is_running:
            try:
                await asyncio.sleep(300)  # Every 5 minutes
                
                # Cleanup memory
                MemoryManager.cleanup()
                
                # Log stats
                mem_usage = MemoryManager.get_memory_usage()
                uptime = datetime.now() - self.start_time
                
                logger.info(f"📈 Maintenance - Uptime: {uptime}, Memory: {mem_usage:.2f} MB")
                
                # Warning jika memory tinggi
                if mem_usage > 200:
                    logger.warning(f"⚠️ High memory usage: {mem_usage:.2f} MB")
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Maintenance task error: {e}")
    
    async def run(self):
        """Main bot running loop"""
        if not await self.initialize():
            return False
        
        self.is_running = True
        
        # Start maintenance task
        maintenance_task = asyncio.create_task(self._periodic_maintenance())
        
        try:
            logger.info("🎯 Starting bot polling...")
            
            # Start polling
            await self.dp.start_polling(
                self.bot,
                skip_updates=True,
                allowed_updates=["message", "callback_query", "chat_member"],
                handle_signals=False
            )
            
            return True
            
        except asyncio.CancelledError:
            logger.info("Bot polling cancelled")
            return False
            
        except Exception as e:
            logger.error(f"Bot polling crashed: {e}", exc_info=True)
            return False
            
        finally:
            self.is_running = False
            
            # Cancel maintenance task
            maintenance_task.cancel()
            try:
                await maintenance_task
            except asyncio.CancelledError:
                pass
            
            # Shutdown
            await self.shutdown()
    
    async def shutdown(self):
        """Graceful shutdown procedure"""
        logger.info("🛑 Initiating shutdown...")
        
        try:
            # Close bot session
            if self.bot:
                await self.bot.session.close()
                logger.info("✅ Bot session closed")
        except Exception as e:
            logger.error(f"Error closing bot session: {e}")
        
        try:
            # Close any HTTP sessions from modules
            from functions.charge_functions import _session
            if _session and not _session.closed:
                await _session.close()
                logger.info("✅ HTTP session closed")
        except:
            pass
        
        # Final memory cleanup
        MemoryManager.cleanup()
        
        # Calculate uptime
        uptime = datetime.now() - self.start_time if self.start_time else "Unknown"
        logger.info(f"📊 Final stats - Uptime: {uptime}, Memory: {MemoryManager.get_memory_usage():.2f} MB")
        logger.info("👋 Shutdown complete")
    
    async def run_with_restart(self):
        """Run bot with auto-restart on failure"""
        while self.restart_count <= self.max_restarts:
            success = await self.run()
            
            if success:
                logger.info("Bot stopped normally")
                break
            else:
                if self.restart_count >= self.max_restarts:
                    logger.error(f"❌ Max restarts reached ({self.max_restarts})")
                    break
                
                # Wait before restart (exponential backoff)
                wait_time = min(30, self.restart_count * 5)
                logger.info(f"⏳ Restarting in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
                
                # Reset for new run
                self.bot = None
                self.dp = None

# ========== MAIN EXECUTION ==========
async def main():
    """Main entry point"""
    bot = ZacatecasBot()
    
    try:
        await bot.run_with_restart()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error in main: {e}", exc_info=True)
    finally:
        logger.info("Process terminated")

def run():
    """Run the bot with proper asyncio setup"""
    # Set event loop policy
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    else:
        asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    
    # Run main function
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot stopped")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        # Wait and try to restart
        import time
        time.sleep(10)
        asyncio.run(main())

if __name__ == "__main__":
    run()