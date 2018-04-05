#!/bin/bash
gpspipe -r|dd count=50|gpsdecode|grep "\"lat\""|logger
