FROM rust:latest as builder

# Don't download Rust docs
# RUN rustup set profile minimal \
    # && rustup update stable

# Create dummy project to build and install dependencies
RUN USER=root cargo new --bin /app
WORKDIR /app

# Copy over manifests and build files
COPY ./Cargo.* ./

# Build dependencies and removes the dummy project
# except for the target folder
RUN cargo build --release
RUN find . -not -path "./target*" -delete

# Copy the entire project
COPY . .

# Build full project
RUN cargo build --release

##### Runtime Image #####
FROM debian:buster-slim

# Install packages
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    openssl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy the built binary
COPY --from=builder /app/target/release/xythrion-webserver .

CMD ["./xythrion-webserver"]
