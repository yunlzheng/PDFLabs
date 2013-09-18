MongoDB DATA Import And Export
--------------------------------------------------

Import collection
==================
mongoimport -h ds041198.mongolab.com:41198 -d heroku_app17595021 -c book -u <user> -p <password> --file <input file>
Export collection
=================
mongoexport -h ds041198.mongolab.com:41198 -d heroku_app17595021 -c book -u <user> -p <password> -o book.json
