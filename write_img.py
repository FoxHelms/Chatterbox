from cassandra.cluster import Cluster

cluster = Cluster()
session = cluster.connect()

session.execute(
    """
    CREATE KEYSPACE IF NOT EXISTS memes WITH REPLICATION = {
        'class' : 'SimpleStrategy',
        'replication_factor' : 1
    }
    """
)

session.execute("USE memes")

create_table_q = session.prepare(
    """
    CREATE TABLE IF NOT EXISTS img_paths (
        id UUID PRIMARY KEY,
        name TEXT,
        img_path TEXT,
        created_at TIMESTAMP,
    );
    """
)

session.execute(create_table_q)

write_q = session.prepare("INSERT INTO img_paths (id, name, img_path) VALUES (uuid(), ?, ?)")
# uuid()


with open('meme_links.txt', 'r') as f:
    meme_links = f.readlines()


batch_size = 100
for i in range(6000):
    img_name = (meme_links[i].split('/',)[-1])
    meme_hash = hash(img_name)
    subdir = str(meme_hash)[-2:]
    meme_name = img_name.split(".jpg")[0]
    img_path = f"/memes/{subdir}/{img_name}"
    session.execute(write_q, [meme_name, img_path])
    if i % batch_size == 0:
        print(f"Scraped: {i} / 6000")

session.close()
