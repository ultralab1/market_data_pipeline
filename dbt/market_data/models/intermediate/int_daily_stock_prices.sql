with daily_values as(
    select *,
    FIRST_VALUE(open_price) OVER(partition by ticker, DATE(fetched_at) order by fetched_at asc) as daily_open,
    LAST_VALUE(close_price) OVER(
        partition by ticker, DATE(fetched_at)
        order by fetched_at asc
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as daily_close
    FROM {{ ref('stage_stock_prices') }}
)
SELECT
    ticker, DATE(fetched_at) as price_date,
    MAX(daily_open) as open_price,
    MAX(high_price) as high_price,
    MIN(low_price) as low_price,
    MAX(daily_close) as close_price,
    SUM(volume) as volume
FROM daily_values
GROUP by 1, 2