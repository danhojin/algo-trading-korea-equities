import gym

class StockDailyPricesEnv(gym.Env):
    """A stock trading environment of historical daily price for OpenAI gym
    """
    metadata = {'render.modes': ['human']}

    def __init__(self, df):
        super().__init__()
        pass

