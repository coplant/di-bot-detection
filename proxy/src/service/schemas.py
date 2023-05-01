from typing import Union

from pydantic import BaseModel


class BrowserSchema(BaseModel):
    duck: Union[str, None] = None
    eval: Union[list, None] = None
    driver: Union[bool, None] = None
    plugin: Union[list, None] = None
    webgl: Union[list, None] = None
    bot: Union[bool, str, None] = None
    ua: Union[list, None] = None


class TimezoneSchema(BaseModel):
    timezone: Union[str, None] = None
    offset: Union[int, None] = None


class FontSchema(BaseModel):
    font_list: Union[list, None] = None
    size: Union[int, None] = None


class CanvasSchema(BaseModel):
    hash: Union[str, int, None] = None


class UserAgentSchema(BaseModel):
    value: Union[str, None] = None
    mobile: Union[bool, None] = None


class ScreenSchema(BaseModel):
    height: Union[int, None] = None
    width: Union[int, None] = None
    inner_height: Union[int, None] = None
    inner_width: Union[int, None] = None
    outer_height: Union[int, None] = None
    outer_width: Union[int, None] = None


class WebRTCSchema(BaseModel):
    value: Union[str, None] = None


class WebGLSchema(BaseModel):
    headless: Union[bool, None] = None
    value: Union[list, None] = None


class LanguageSchema(BaseModel):
    value: Union[list, None] = None


class FingerprintSchema(BaseModel):
    browser: Union[BrowserSchema, None] = None
    timezone: Union[TimezoneSchema, None] = None
    fonts: Union[FontSchema, None] = None
    canvas: Union[CanvasSchema, None] = None
    UA: Union[UserAgentSchema, None] = None
    screen: Union[ScreenSchema, None] = None
    webRTC: Union[WebRTCSchema, None] = None
    webGL: Union[WebGLSchema, None] = None
    language: Union[LanguageSchema, None] = None
