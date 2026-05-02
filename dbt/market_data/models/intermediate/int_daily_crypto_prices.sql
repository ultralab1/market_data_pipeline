with daily_values as (
    select *,
    first_value(price) over(partition by symbol, date(fetched_at) order by fetched_at asc) as daily_open,
    last_value(price) over(
    partition by symbol, date(fetched_at)
    order by fetched_at asc
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as daily_close
    from {{ ref('stage_crypto_prices') }}
)
select
    symbol, date(fetched_at) as price_date,
    MAX(daily_open) as open_price,
    MAX(price) as high_price,
    MIN(price) as low_price,
    MAX(daily_close) as close_price,
    MAX(total_volume) as volume
FROM daily_values
GROUP by 1, 2