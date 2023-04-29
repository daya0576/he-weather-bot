dev:
	echo "dev"
	fly dev local 

release:
	poetry export -f requirements.txt --without-hashes --output requirements.txt
	git push heroku master
