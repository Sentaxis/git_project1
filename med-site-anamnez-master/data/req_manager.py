from typing import Union
import flask


__json_stack = []


def get_json():
    if __json_stack:
        return __json_stack[-1]


def set_json(json: Union[dict, list, None]):
    ("""После вызова set_json сразу вызвать """
     """нужную функцию API, чтобы в ней """
     """произошёл 'pop' из стэка""")
    # на самом деле скорее append_json,
    # но такое название лучше, учитывая
    # как эту функцию будут использовать
    __json_stack.append(json)


def del_json():
    if __json_stack:
        del __json_stack[-1]


def simulate_request(method: str):
    if not __json_stack:
        return None
    last_json = get_json()
    del_json()
    req = flask.Request.from_values(
        method=method, json=last_json)
    return req


def get_request(method: str):
    ("""Для передачи json параметров """
     """в route при вызове его, как обычную """
     """функцию, для переиспользования REST API """
     """без использования модуля requests""")
    req = simulate_request(method)
    if req is None:
        req = flask.request
    return req
