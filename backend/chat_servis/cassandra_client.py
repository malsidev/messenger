from cassandra.cluster import Cluster


class Cassandra:

    def __init__(self):
        self.cluster = None
        self.session = None


    async def connect(self):

        self.cluster = Cluster(
            ["cassandra"],
            port=9042
        )

        self.session = self.cluster.connect()

        self.session.set_keyspace(
            "messenger"
        )

        print("Cassandra started")


    async def close(self):

        if self.cluster:
            self.cluster.shutdown()

        print("Cassandra stopped")


cassandra = Cassandra()