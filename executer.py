#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import sys


def execute_snippet(snippet, globals):
    """Temporary changes the standard output stream to capture exec output"""
    temp_buffer = io.StringIO()

    sys.stdout = temp_buffer
    exec(snippet, globals)
    sys.stdout = sys.__stdout__
    
    return temp_buffer.getvalue()
