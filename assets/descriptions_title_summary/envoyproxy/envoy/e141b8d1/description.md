# Remove legacy load balancer constructors and configuration classes

Consolidate dual configuration system for load balancers (round robin, random, least request, maglev, ring hash) by removing legacy config classes and constructors. Convert legacy cluster proto configurations directly to typed config classes at load time.