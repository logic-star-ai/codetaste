#!/bin/bash
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Shell environment setup script for Apache ShenYu
# This script should be sourced: source /scripts/setup_shell.sh

# Set Java 17 as the JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH="$JAVA_HOME/bin:$PATH"

# Set encoding to UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Maven options
export MAVEN_OPTS="-Xmx2048m -XX:MaxMetaspaceSize=512m"

# Navigate to the project directory
cd /testbed || exit 1

# Check if project is already installed (to make script idempotent)
# We check for a marker file to avoid rebuilding unnecessarily
if [ ! -f "$HOME/.shenyu_installed" ]; then
    echo "Installing project dependencies (first run)..."
    # Install the project without running tests
    ./mvnw -B clean install \
        -DskipTests \
        -Drat.skip=true \
        -Dmaven.javadoc.skip=true \
        -Djacoco.skip=true \
        -Dcheckstyle.skip=true \
        2>&1 | tail -30

    # Check if install was successful
    if [ $? -eq 0 ]; then
        touch "$HOME/.shenyu_installed"
        echo "Project installed successfully"
    else
        echo "Project installation failed"
        return 1
    fi
else
    echo "Project already installed, skipping installation"
fi

echo "Environment configured successfully"
echo "Java version: $(java -version 2>&1 | head -1)"
echo "Maven version: $(./mvnw --version 2>&1 | head -1)"
