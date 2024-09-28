FROM openjdk:11-jdk-slim

# Update and install necessary dependencies
RUN apt-get update && \
    apt-get install -y software-properties-common gnupg2 wget && \
    apt-get clean

# Set up locale and timezone
RUN apt-get update && apt-get install -y locales tzdata && \
    locale-gen en_US.UTF-8 && \
    ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

# Install Python 3.9
RUN apt-get update && \
    apt-get install -y python3.9 python3.9-distutils python3.9-dev && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    python3.9 get-pip.py && \
    rm get-pip.py && \
    ln -s /usr/bin/python3.9 /usr/local/bin/python && \
    ln -s /usr/bin/python3.9 /usr/local/bin/python3 && \
    apt-get clean

# Verify Python and Java versions
RUN python --version && java -version

# Install PySpark
RUN pip install pyspark==3.2.0 pandas

# Clean up
RUN apt-get autoremove -y && apt-get clean

# Create app directory
RUN mkdir /app

# Copy the application code
COPY app /app

# Download PostgreSQL JDBC driver
RUN wget https://jdbc.postgresql.org/download/postgresql-42.2.23.jar -O /app/postgresql-42.2.23.jar

# Set the working directory
WORKDIR /app

# Run the application
CMD ["python", "main.py"]