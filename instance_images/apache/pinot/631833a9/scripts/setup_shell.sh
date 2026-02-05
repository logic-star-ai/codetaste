#!/bin/bash
#
# Shell environment setup script for Apache Pinot
# This script must be sourced: source /scripts/setup_shell.sh
# It configures the shell environment and installs project dependencies

set -e

# Set Java 11 as the default Java version
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

# Set Maven options for build and test
export MAVEN_OPTS="-Xmx2G -DskipShade -DfailIfNoTests=false -Dmaven.wagon.httpconnectionManager.ttlSeconds=25 -Dmaven.wagon.http.retryHandler.count=30 -Dhttp.keepAlive=false -Dmaven.wagon.http.pool=false -B -ntp -XX:+IgnoreUnrecognizedVMOptions --add-exports=jdk.compiler/com.sun.tools.javac.api=ALL-UNNAMED --add-exports=jdk.compiler/com.sun.tools.javac.file=ALL-UNNAMED --add-exports=jdk.compiler/com.sun.tools.javac.parser=ALL-UNNAMED --add-exports=jdk.compiler/com.sun.tools.javac.tree=ALL-UNNAMED --add-exports=jdk.compiler/com.sun.tools.javac.util=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED"

# Environment variables for testing
export RUN_INTEGRATION_TESTS=false
export RUN_TEST_SET=1

# Change to testbed directory
cd /testbed

# Build the project (install dependencies and compile)
# Run testset 1 build which includes core modules
echo "Building Apache Pinot project..."
./mvnw clean install \
  -DskipTests -Dcheckstyle.skip -Dspotless.skip -Denforcer.skip -Dlicense.skip -Dmaven.plugin.appassembler.skip=true \
  -am -B -T 16 -ntp \
  -P github-actions \
  -pl 'pinot-spi' \
  -pl 'pinot-segment-spi' \
  -pl 'pinot-common' \
  -pl 'pinot-segment-local' \
  -pl 'pinot-core' \
  -pl 'pinot-query-planner' \
  -pl 'pinot-query-runtime' 2>&1 | tail -100

echo "Build complete. Environment ready for testing."
