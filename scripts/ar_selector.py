import json
import os
from typing import List
from dataclasses import dataclass

import gradio as gr

import modules.scripts as scripts
from modules.ui_components import ToolButton

BASE_DIR = scripts.basedir()
# load settings
SETTING_PATH = os.path.join(BASE_DIR, "settings.json")


@dataclass
class Settings:
    
    sdxl_aspect_ratios: List[str]

    @classmethod
    def load_config(cls):
        try:
            with open(SETTING_PATH, "r") as f:
                settings = json.load(f)
                cls.sdxl_aspect_ratios = settings["sdxl_aspect_ratios"]

                return cls
        except FileNotFoundError:
            ext_name = os.path.basename(BASE_DIR)
            print(
                f"[{ext_name}] Setting file not found. Please reinstall this extension."
            )


settings = Settings.load_config()

class AspectRatioSelectorScript(scripts.Script):
    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def title(self):
        return "SDXL Aspect Ratio Selector"

    def ui(self, is_img2img):
        def handle_ar_select(radio):
            w, h = radio.split("*")

            return (w, h)

        if is_img2img: 
            w, h = self.i2i_w, self.i2i_h
        else:
            w, h = self.t2i_w, self.t2i_h

        with gr.Accordion(label="SDXL Aspect Ratio Selector", open=True):
            radio = gr.Radio(settings.sdxl_aspect_ratios, label='width * height', value='{w}*{h}')
            radio.change(
                handle_ar_select, inputs=[radio], outputs=[w, h]
            )

    ## Function to update the values in appropriate Width/Height fields
    # https://github.com/AUTOMATIC1111/stable-diffusion-webui/pull/7456#issuecomment-1414465888
    def after_component(self, component, **kwargs):
        if kwargs.get("elem_id") == "txt2img_width":
            self.t2i_w = component
        if kwargs.get("elem_id") == "txt2img_height":
            self.t2i_h = component
        if kwargs.get("elem_id") == "img2img_width":
            self.i2i_w = component
        if kwargs.get("elem_id") == "img2img_height":
            self.i2i_h = component
