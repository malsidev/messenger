import time

from cassandra.cluster import Cluster


class CassandraClient:
    def __init__(self):
        while True:
            try:
                self.cluster = Cluster(
                    ["cassandra"],
                    port=9042,
                )

                self.session = self.cluster.connect()
                self.session.set_keyspace("messenger")
                break
            except Exception as e:
                print("Waiting Cassandra...", e)
                time.sleep(5)



cassandra = CassandraClient()