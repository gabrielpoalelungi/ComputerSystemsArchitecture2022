#! /bin/bash
sudo kill $(ps aux | grep "/bin/bash" | cut -d' ' -f4 | head -n1)
