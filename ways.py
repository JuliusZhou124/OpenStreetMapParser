import osmium as osm
import csv

class NodeLocationsForWay(osm.SimpleHandler):
    def __init__(self, node_locations):
        osm.SimpleHandler.__init__(self)
        self.node_locations = node_locations

    def node(self, n):
        self.node_locations[n.id] = (n.location.lat, n.location.lon)

class OSMHandler(osm.SimpleHandler):
    def __init__(self, node_locations):
        osm.SimpleHandler.__init__(self)
        self.ways = []
        self.node_locations = node_locations

    def way(self, w):
        highway_type = None
        for tag in w.tags:
            if tag.k == "highway":
                highway_type = tag.v
                break
        # if "highway" in [tag.k for tag in w.tags]:
        #     highway_type = next((tag.v for tag in w.tags if tag.k == "highway"), None)
        if highway_type in ["crossing", "traffic_signal", "stop", "residential", "tertiary", "service"]:
            nodes = w.nodes
            for i in range(0, len(nodes) - 1):
                start_node = nodes[i]
                end_node = nodes[i + 1]
                start_lat, start_lon = self.node_locations[start_node.ref]
                end_lat, end_lon = self.node_locations[end_node.ref]
                self.ways.append((start_node.ref, start_lat, start_lon, end_node.ref, end_lat, end_lon))

if __name__ == "__main__":
    node_locations = {}
    node_handler = NodeLocationsForWay(node_locations)
    osmhandler = OSMHandler(node_locations)

    node_handler.apply_file("outer-berkeley.osm")
    osmhandler.apply_file("outer-berkeley.osm")

    with open("ways.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "lat_start", "lon_start", "id_end", "lat_end", "lon_end"])  # header row
        writer.writerows(osmhandler.ways)