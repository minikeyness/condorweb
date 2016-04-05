from .condor_collect import collector
from .condor_sched import schedd

status_enum = schedd.factory.create("StatusCode")
universe_enum = schedd.factory.create("UniverseType")
hash_enum = schedd.factory.create("HashType")
