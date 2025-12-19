#!/bin/bash
mkdir -p data
uvicorn app.main:app --reload
