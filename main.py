import osmium as osm
import pandas as pd

class OSMHandler(osm.SimpleHandler):
    def __init__(self):
        osm.SimpleHandler.__init__(self)
        self.osm_data = []

    def tag_inventory(self, elem, elem_type):
        for tag in elem.tags:
            self.osm_data.append([elem_type, 
                                   elem.id, 
                                   elem.version,
                                   elem.visible,
                                   pd.Timestamp(elem.timestamp),
                                   elem.uid,
                                   elem.user,
                                   elem.changeset,
                                   len(elem.tags),
                                   tag.k, 
                                   tag.v])

    def node(self, n):
        self.tag_inventory(n, "node")

    def way(self, w):
        self.tag_inventory(w, "way")

    def relation(self, r):
        self.tag_inventory(r, "relation")

if __name__ == "__main__":
    
    osmhandler = OSMHandler()
    # scan the input file and fills the handler list accordingly
    osmhandler.apply_file("berkeley-map-northwest.osm")

    # transform the list into a pandas DataFramex
    data_colnames = ['type', 'id', 'version', 'visible', 'ts', 'uid',
                    'user', 'chgset', 'ntags', 'tagkey', 'tagvalue']
    df_osm = pd.DataFrame(osmhandler.osm_data, columns=data_colnames)
    df_osm = df_osm.sort_values(by=['type', 'id', 'ts'])

    print(df_osm)

