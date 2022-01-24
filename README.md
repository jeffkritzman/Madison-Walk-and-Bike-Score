# Madison-Walk-and-Bike-Score

Created in Python, using Bing Location API and WalkScore API. To reuse, you will need API keys for each of these. If there aren't relevant water features in your desired area, you may not need the Bing API. I included this part of the code mostly to identify lakes, as Madison has lots of water.

The WalkScore API has a daily limit of 5,000 calls for the free version. As such, I chunked the region I wanted into smaller chunks. This is why I have dayNum, with multiple files being created once daily.

Tableau Public visualization of the resulting data set:
https://public.tableau.com/app/profile/jeff.kritzman/viz/MadisonWalkBikeScores/MadisonWalkBikeScore
