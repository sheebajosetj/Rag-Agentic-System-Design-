# scheduler.py

import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from updater import run_pipeline

async def job_wrapper():
    await run_pipeline()

async def main():
    scheduler = AsyncIOScheduler()
    
    # Schedule the async job
    scheduler.add_job(job_wrapper, 'interval', seconds=10)
    
    scheduler.start()
    print("Scheduler started. Press Ctrl+C to stop.")
    
    # Keep the loop alive
    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        print("Shutting down scheduler...")
        scheduler.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
