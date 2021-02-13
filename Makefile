dev:
	echo "dev"
	heroku local web

release:
	poetry export -f requirements.txt --without-hashes --output requirements.txt
	git push heroku master