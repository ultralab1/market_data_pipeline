SELECT
    ticker,
    CAST(timestamp as timestamptz) as fetched_at,
    CAST(open as numeric) as open_price,
    CAST(high as numeric) as high_price,
    CAST(low as numeric) as low_price,
    CAST(close as numeric) as close_price,
    CAST(volume as BIGINT) as volume
FROM raw.stock_prices
WHERE close > 0