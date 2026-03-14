# run_24hours.py - KPX 예보 + KMA 과거/예보 통합 (24시간 주기)
import sys
import logging
from datetime import datetime, timedelta

from data_pipeline import daily_forecast_and_predict, daily_historical_update   # ← 현재 위치한 파일명으로 수정

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)
def run():
    now = datetime.now()

    # 예보: 오늘 ~ 내일
    forecast_start = now.strftime('%Y-%m-%d')
    forecast_end = (now + timedelta(days=1)).strftime('%Y-%m-%d')

    # 실측: 어제 ~ 오늘 (미래 날짜 불가 제한 때문에 반드시 오늘 이하)
    hist_start = (now - timedelta(days=1)).strftime('%Y-%m-%d')
    hist_end = now.strftime('%Y-%m-%d')

    logger.info(f"=== 예보 업데이트: {forecast_start} ~ {forecast_end} ===")
    logger.info(f"=== 실측 업데이트: {hist_start} ~ {hist_end} ===")

    try:
        daily_forecast_and_predict(forecast_start, forecast_end)
        daily_historical_update(hist_start, hist_end)
        logger.info("24시간 업데이트 완료 ✅")

    except Exception as e:
        logger.error(f"오류 발생: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    run()