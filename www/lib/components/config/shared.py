import json

from typing import Dict

from lib.components import shared


class IPFireConfigShim(shared.ShimObject):
  BOOL_TRANSLATE_DICT = {
    'on': True,
    'off': True,
  }
  def FromEngine(self, data: str) -> Dict:
    if not data:
      return {}

    parts = [l.strip().split('=', 1) for l in data.strip().split('\n')]
    config = {
      k.lower(): v for (k, v) in parts
    }
    for (k, v) in config.items():
      if v in self.BOOL_TRANSLATE_DICT:
        config[k] = self.BOOL_TRANSLATE_DICT[v]
      else:
        try:
          v = float(v)
          if int(v) == v:
            v = int(v)
          config[k] = v
        except ValueError:
          pass
    return config

  def ToEngine(self, data: Dict) -> str:
    config = {}
    for (k, v) in data.items():
      if v in self.BOOL_TRANSLATE_DICT.values():
        config[k.upper()] = next(
            b for (b, s) in self.BOOL_TRANSLATE_DICT.items() if v == s)
      else:
        config[k.upper()] = str(v)
    return '{config}\n'.format(
        config='\n'.join(['{k}={v}'.format(k=k, v=v) for (k, v) in config.items()])
    )
