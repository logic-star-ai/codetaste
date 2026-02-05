#!/bin/bash
# Shell environment setup script for Ghidra
# This script configures the shell environment for building and testing
# Must be sourced, not executed

set -e

# Determine the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Set up Java 11
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

# Set up Gradle 5.0
export GRADLE_HOME=/opt/gradle-5.0
export PATH=$GRADLE_HOME/bin:$PATH

# Verify Java version
echo "Java version:"
java -version

# Verify Gradle version
echo "Gradle version:"
gradle --version | head -5

# Set up Gradle init script for repositories
mkdir -p ~/.gradle/init.d
cat > ~/.gradle/init.d/repos.gradle << 'EOF'
ext.HOME = System.getProperty('user.home')

allprojects {
    repositories {
        mavenCentral()
        jcenter()
        flatDir name:'flat', dirs:["$HOME/flatRepo"]
    }
}
EOF

# Create flatRepo directory if it doesn't exist
mkdir -p ~/flatRepo

# Download and setup required dependencies in flatRepo
cd ~/flatRepo

# Download dex2jar dependencies if not present
if [ ! -f "dex-ir-2.0.jar" ]; then
    echo "Downloading dex2jar dependencies..."
    cd /tmp
    wget -q https://github.com/pxb1988/dex2jar/releases/download/2.0/dex-tools-2.0.zip
    unzip -q dex-tools-2.0.zip
    cp dex2jar-2.0/lib/dex-*.jar ~/flatRepo/
    rm -rf dex-tools-2.0.zip dex2jar-2.0
fi

# Download AXMLPrinter2.jar if not present
if [ ! -f ~/flatRepo/AXMLPrinter2.jar ]; then
    echo "Downloading AXMLPrinter2.jar..."
    cd ~/flatRepo
    wget -q https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/android4me/AXMLPrinter2.jar
fi

# Download HFSExplorer dependencies if not present
if [ ! -f ~/flatRepo/hfsx.jar ]; then
    echo "Downloading HFSExplorer dependencies..."
    cd /tmp
    wget -q https://sourceforge.net/projects/catacombae/files/HFSExplorer/0.21/hfsexplorer-0_21-bin.zip
    unzip -q hfsexplorer-0_21-bin.zip
    cp lib/*.jar ~/flatRepo/
    rm -rf hfsexplorer-0_21-bin.zip lib
fi

# Download baksmali if not present (using 2.0.3 as 1.4.0 is not available)
if [ ! -f ~/flatRepo/baksmali-1.4.0.jar ]; then
    echo "Downloading baksmali..."
    cd ~/flatRepo
    wget -q https://repo1.maven.org/maven2/org/smali/baksmali/2.0.3/baksmali-2.0.3.jar
    cp baksmali-2.0.3.jar baksmali-1.4.0.jar
fi

# Change to testbed directory
cd /testbed

# Run prepDev to prepare the development environment
# This generates source files, indexes help, and unpacks dependencies
# Exclude GhidraDev plugin tasks as they require Eclipse dependencies
echo "Running prepDev to prepare development environment..."
gradle prepDev -x yajswDevUnpack -x :GhidraDevPlugin:cdtUnpack -x :GhidraDevPlugin:pyDevUnpack --console=plain 2>&1 | tail -20

echo "Environment setup complete!"
echo "JAVA_HOME: $JAVA_HOME"
echo "GRADLE_HOME: $GRADLE_HOME"
