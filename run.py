#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apps import create_app

app = create_app()
app.debug = True
app.run(host='localhost')
