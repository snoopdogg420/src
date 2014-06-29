# Window options...
window-title Toontown Infinite
win-origin -1 -1

# Filenames/filepaths...
icon-filename icon.ico
cursor-filename phase_3/etc/toonmono.cur
preferences-filename preferences.gz

model-path ../ToontownInfiniteResources
model-cache-models #f
model-cache-textures #f

default-model-extension .bam

# Audio...
audio-library-name p3fmod_audio

# Database...
account-server-endpoint https://www.toontowninfinite.com/api/
accountdb-type developer
account-bridge-filename astron/databases/account-bridge.db
account-server-min-access-level 600

# Server...
server-force-ssl 0
server-port 7198
server-version infinite-dev
server-timezone US/Eastern

eventlog-host 127.0.0.1

# DClass files (in reverse order)...
dc-file astron/dclass/toon.dc
dc-file astron/dclass/otp.dc

# Performance
hardware-animated-vertices #t
preload-avatars #t
sync-video #f
smooth-lag 0.4
ai-sleep 0.01

# Coverage
want-pstats 0

# Egg ObjectTypes...
egg-object-type-barrier <Scalar> collide-mask { 0x01 } <Collide> { Polyset descend }
egg-object-type-trigger <Scalar> collide-mask { 0x01 } <Collide> { Polyset descend intangible }
egg-object-type-sphere <Scalar> collide-mask { 0x01 } <Collide> { Sphere descend }
egg-object-type-trigger-sphere <Scalar> collide-mask { 0x01 } <Collide> { Sphere descend intangible }
egg-object-type-floor <Scalar> collide-mask { 0x02 } <Collide> { Polyset descend }
egg-object-type-dupefloor <Scalar> collide-mask { 0x02 } <Collide> { Polyset keep descend }
egg-object-type-camera-collide <Scalar> collide-mask { 0x04 } <Collide> { Polyset descend }
egg-object-type-camera-collide-sphere <Scalar> collide-mask { 0x04 } <Collide> { Sphere descend }
egg-object-type-camera-barrier <Scalar> collide-mask { 0x05 } <Collide> { Polyset descend }
egg-object-type-camera-barrier-sphere <Scalar> collide-mask { 0x05 } <Collide> { Sphere descend }

# The modelers occasionally put <ObjectType> { model } instead of <Model> { 1 }...
egg-object-type-model <Model> { 1 }
egg-object-type-dcs <DCS> { 1 }

# Safe zones...
want-safe-zones #t
want-toontown-central #t
want-donalds-dock #f
want-daisys-garden #f
want-minnies-melodyland #f
want-the-burrrgh #f
want-donalds-dreamland #f
want-goofy-speedway #f
want-outdoor-zone #f
want-golf-zone #f

# Cog headquarters...
want-cog-headquarters #f
want-sellbot-headquarters #f
want-cashbot-headquarters #f
want-lawbot-headquarters #f
want-bossbot-headquarters #f

want-treasure-planners #f
want-suit-planners #t
want-butterflies #f

# Classic characters...
want-classic-chars #f
want-mickey #f
want-donald-dock #f
want-daisy #f
want-minnie #f
want-pluto #f
want-donald-dreamland #f
want-chip-and-dale #f
want-goofy #f

# Minigames...
want-minigames #f
want-race-game #f
want-cannon-game #f
want-tag-game #f
want-pattern-game #f
want-ring-game #f
want-maze-game #f
want-tug-game #f
want-catch-game #f
want-diving-game #f
want-target-game #f
want-pairing-game #f
want-vine-game #f
want-ice-game #f
want-thief-game #f
want-2d-game #f
want-photo-game #f
want-travel-game #f
force-minigame 0

# Cog buildings...
want-cogbuildings #t
silly-street-building-min 14
silly-street-building-max 14
silly-street-building-chance 100.0
loopy-lane-building-min 14
loopy-lane-building-max 14
loopy-lane-building-chance 100.0
punchline-place-building-min 14
punchline-place-building-max 14
punchline-place-building-chance 100.0
barnacle-boulevard-building-min 1
barnacle-boulevard-building-max 5
barnacle-boulevard-building-chance 75.0
seaweed-street-building-min 1
seaweed-street-building-max 5
seaweed-street-building-chance 75.0
lighthouse-lane-building-min 1
lighthouse-lane-building-max 5
lighthouse-lane-building-chance 75.0
elm-street-building-min 2
elm-street-building-max 6
elm-street-building-chance 90.0
maple-street-building-min 2
maple-street-building-max 6
maple-street-building-chance 90.0
oak-street-building-min 2
oak-street-building-max 6
oak-street-building-chance 90.0
alto-avenue-building-min 3
alto-avenue-building-max 7
alto-avenue-building-chance 95.0
baritone-boulevard-building-min 3
baritone-boulevard-building-max 7
baritone-boulevard-building-chance 95.0
tenor-terrace-building-min 3
tenor-terrace-building-max 7
tenor-terrace-building-chance 95.0
walrus-way-building-min 5
walrus-way-building-max 10
walrus-way-building-chance 100.0
sleet-street-building-min 5
sleet-street-building-max 10
sleet-street-building-chance 100.0
polar-place-building-min 5
polar-place-building-max 10
polar-place-building-chance 100.0
lullaby-lane-building-min 6
lullaby-lane-building-max 12
lullaby-lane-building-chance 100.0
pajama-place-building-min 6
pajama-place-building-max 12
pajama-place-building-chance 100.0

# Cashbot boss...
want-resistance-toonup #f
want-resistance-restock #f
want-resistance-money #t
want-resistance-dance #f

# Picnic table board games...
want-game-tables #f
want-checkers #f
want-chinese-checkers #f
want-find-four #f

# True friends...
parent-password-set #t
allow-secret-chat #t

# Core features...
want-fishing #f
want-housing #f
want-pets #f
want-karts #f
want-parties #f
want-cogdominiums #f
want-boarding-groups #f
want-achievements #f

# Optional...
show-total-population #t
want-mat-all-tailors #t
want-news-page #f
want-news-tab #f
want-long-pattern-game #f
want-talkative-tyler #f

# Developer options...
want-dev #f
want-tailor-jellybeans #f
want-instant-parties #t

# Temporary...
want-old-fireworks #t
