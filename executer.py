#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import sys
import copy

import timeout_decorator


@timeout_decorator.timeout(5, use_signals=False)  # some dumb security
def execute_snippet(snippet, globals_wrapper):
    """Temporary changes the standard output stream to capture exec output"""
    existing_names = set(globals_wrapper.keys())

    temp_buffer = io.StringIO()
    sys.stdout = temp_buffer
    exec(snippet, globals_wrapper)
    sys.stdout = sys.__stdout__

    new_names = {k: v for k, v in globals_wrapper.items() if k not in existing_names}
    return temp_buffer.getvalue(), new_names  # we need it to support multithreading
