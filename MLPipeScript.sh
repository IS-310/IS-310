#! /bin/bash

if python3 dataAnalysis.py; then
	python3 dataAnalysis.py | python3 MLPipeIn.py
else
	echo "Dataframe size < 10. Wait abit more"
fi

 
