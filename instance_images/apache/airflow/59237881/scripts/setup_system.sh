#!/bin/bash
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# System-level setup script for Apache Airflow
# This script performs runtime system configuration (e.g., starting services)
# It must be executed with sudo.

set -e

# Install system dependencies needed for Python packages
# These are required for building Python packages like mysqlclient, psycopg2, etc.
export DEBIAN_FRONTEND=noninteractive

# Update package list and install dependencies
apt-get update -qq
apt-get install -y -qq \
    libmysqlclient-dev \
    pkg-config \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    libkrb5-dev \
    libsasl2-dev \
    libldap2-dev \
    > /dev/null 2>&1 || true

# For SQLite-based tests, no system services need to be started
# If we were to use PostgreSQL/MySQL/Redis, we would start them here

exit 0
