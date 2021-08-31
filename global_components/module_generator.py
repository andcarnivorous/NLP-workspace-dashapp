import os
from configs.module_templates import main_module_code, layout_module_code
from utils import generate_logger

logger = generate_logger(__name__)


class ModuleGenerator:

    def __init__(self, pwd, module_name):
        self.pwd = pwd
        self.module_name = module_name
        # TODO: Check module name only contains alpha and underscores
        self.files_to_generate = [f"{self.module_name}/__init__.py",
                                  f"{self.module_name}/{self.module_name}.py",
                                  f"{self.module_name}/{self.module_name}_layout.py"]

    def create_new_modules(self):
        logger.info("Generating new module directory and files...")
        os.mkdir(self.module_name)
        for file in self.files_to_generate:
            with open(file, "w") as module_file:
                module_file.write("")

    def fill_main_module(self):
        with open(self.files_to_generate[1], "w") as file:
            file.write(main_module_code % self.module_name)

    def fill_layout_module(self):
        with open(self.files_to_generate[2], "w") as file:
            file.write(layout_module_code % (self.module_name, self.module_name, self.module_name))

    def generate_new_module(self):
        self.create_new_modules()
        logger.info("Creating templates for new module files...")
        self.fill_main_module()
        self.fill_layout_module()
        logger.info("New dash module created")

