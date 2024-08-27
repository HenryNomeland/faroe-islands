/*
Overpass Turbo search by HZN
*/
[out:csv(::id, ::lat, ::lon, "name", "place")][timeout:25];
// getting search area
area(id:3600052939)->.searchArea;
// outputting results
nwr["place"~"^(town|village)$",i](area.searchArea);
out geom;