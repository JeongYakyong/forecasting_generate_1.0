# run_3hours.py - KPX 실적 데이터 수집 (3시간 주기)
import sys
import logging
from datetime import datetime, timedelta
from api_fetchers import (
    fetch_kpx_past,
    fetch_kpx_future,
    fetch_kpx_historical,
    fetch_kma_past_asos,
    fetch_kma_future_ncm
)
from db_manager import JejuEnergyDB

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

def run():
    now = datetime.now()
    # 오늘 포함 최근 2일치 수집 (데이터 지연 감안)
    start_date = (now - timedelta(days=1)).strftime('%Y-%m-%d')
    end_date = now.strftime('%Y-%m-%d')
    
    logger.info(f"=== KPX 실적 수집 시작: {start_date} ~ {end_date} ===")
    
    try:
        df = fetch_kpx_past(start_date, end_date)
        
        if df.empty:
            logger.warning("수집된 데이터가 없습니다. 종료.")
            sys.exit(0)
        
        logger.info(f"수집 완료: {len(df)}행")
        
        db = JejuEnergyDB()
        db.save_historical(df)
        db.close()
        
        logger.info("DB 저장 완료 ✅")
        
    except Exception as e:
        logger.error(f"오류 발생: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    run()