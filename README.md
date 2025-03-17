# geohash-polygon-py

A python implementation to find the geohashes inside a polygon. Used in
my [GeoLens Project](http://www.cs.colostate.edu/geolens) to decide the GeoHash tiles to display. Many classes
have been reduced to improve readability and to inspire usability.

This project is inspired [from](https://github.com/derrickpelletier/geohash-poly) and
my [java implementation](https://github.com/jaredkoontz/GeoHashesInPolygon/)

however, it uses a home-brewed method to find the resolution of the geohashes to display. This method is called the
longest enclosing hash. In this algorithm, we find the smallest geohash tile that would fully enclose the geohash. More
information about this can be found in
our [publications](http://www.cs.colostate.edu/geolens/entry/publications/publications.php)
