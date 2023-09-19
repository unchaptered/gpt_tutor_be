import os
import yaml
from typing import Optional

# common
from common.types.config.config_type import ConfigType


class ConfigProvider():

    config: Optional[ConfigType] = None

    def __init__(self) -> None:
        pass

    def loadConfig(self):

        path = 'config.yml'
        try:
            abs_path = os.getcwd()

            with open(os.path.join(abs_path, path), encoding='utf-8') as stream:
                return yaml.safe_load(stream)

        except yaml.YAMLError as yaml_e:
            raise Exception('잘못된 형식의 YAML 입니다.')

        except Exception as e:
            print(e)
            raise Exception('파일을 찾지 못했습니다.')

    def getConfig(self) -> ConfigType:
        if self.config is None:
            self.config = self.loadConfig()

        return self.config


configProvider = ConfigProvider()
