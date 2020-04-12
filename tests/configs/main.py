import tests.configs.local as local

class Config:
  value = None

  @classmethod
  def init(cls, env):
    # Switch env here
    cls.value = local.value