#!/bin/bash
apt-get update && apt-get install -y ffmpeg
streamlit run beru.py --server.port=$PORT --server.enableCORS=false
