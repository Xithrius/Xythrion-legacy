use std::io::Result;

use actix_web::{get, App, HttpServer, Responder};

#[get("/ping")]
async fn ping() -> impl Responder {
    "pong!".to_string()
}

#[actix_web::main]
async fn main() -> Result<()> {
    HttpServer::new(|| App::new().service(ping))
        .bind(("127.0.0.1", 8090))
        .unwrap()
        .run()
        .await
}
