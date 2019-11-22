# office-location-project
I recently created a new company in the `GAMING industry`. The company will have the following scheme:

- 20 Designers
- 5 UI/UX Engineers
- 10 Frontend Developers
- 15 Data Engineers
- 5 Backend Developers
- 20 Account Managers
- 1 Maintenance guy that loves basketball
- 10 Executives
- 1 CEO/President

As a data engineer I have asked all the employees to show their preferences on where to place the new office.
My goal is to place the **new company offices** in the best place for the company to grow.
I must found a place that more or less covers all the following requirements:

- Designers like to go to design talks and share knowledge. There must be some nearby companies that also do design.
- 30% of the company have at least 1 child.
- Developers like to be near successful tech startups that have raised at least 1 Million dollars.
- Executives like Starbucks A LOT. Ensure there's a starbucks not to far.
- Account managers need to travel a lot
- All people in the company have between 25 and 40 years, give them some place to go to party.
- Nobody in the company likes to have companies with more than 10 years in a radius of 2 KM.
- The CEO is Vegan

For that, I have created an **office location recommender**. You can find it on `main.ipynb`.

## Details:
- I have imported into my localhost MongoDB a Crunchbase startups database. You can do it on your own with `./input/companies.json` running this command: 

        `mongoimport --db companies --collection companies --file companies.json`

- I have used Google Places API to find out if some of the companies I want to have close to mine are near to starbucks, day care centers, airports, nightclubs, vegan restaurants, etc.
- Combining MongoDB data and Google Places API data I have created a Pandas DataFrame with all the ideal locations per city that fit my need. Checkout `src/googlePlacesAPI.py` and `src/pymongo.py`.
- Finally, I have created a **office location recommender** in `main.ipynb`, where you can paint in a map all the ideal locations for the new office and also the locations of the services we want to have close to us.