#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import sys


def execute_snippet(new_code, code):
    """Temporary changes the standard output stream to capture exec output"""
    # just execute the existing code, without stream redirection
    exec(code)
    # execute new code, capture output
    temp_buffer = io.StringIO()
    sys.stdout = temp_buffer
    exec(new_code)
    sys.stdout = sys.__stdout__

    return temp_buffer.getvalue(), '{}\n{}'.format(code, new_code)
