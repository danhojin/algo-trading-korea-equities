from gym.envs.registration import register

register(
    id='StockDailyPrices-v0',
    entry_point='krx_stock.env:StockDailyPricesEnv',
)
