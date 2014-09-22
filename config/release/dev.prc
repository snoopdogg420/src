# Distribution token...
distribution dev

# Models/textures...
model-path ../resources

# Server...
server-version infinite-dev
client-agents 1
server-force-ssl #f

# RPC...
want-rpc-server #t
rpc-server-endpoint http://localhost:8080/

# DClass files (in reverse order)...
dc-file astron/dclass/toon.dc
dc-file astron/dclass/otp.dc

# Database...
accountdb-type developer
account-server-min-access-level 600

# Core features...
want-pets #f
want-parties #f
want-cogdominiums #f
want-achievements #f
want-whitelist #f

# Districts...
shard-low-pop 50
shard-mid-pop 100

# Picnic table board games...
want-find-four #f

# Optional...
want-yin-yang #t
want-chestnut-park-construction #t

# Developer options...
want-instant-parties #t
