use std::io::Result;

use actix_web::{
    get,
    web::{Either, Form, Json},
    App, HttpServer, Responder,
};

use serde::Deserialize;

#[get("/ping")]
async fn ping() -> impl Responder {
    "pong!".to_string()
}

#[derive(Deserialize)]
struct Register {
    username: String,
    country: String,
}

#[get("/register")]
async fn register(form: Either<Json<Register>, Form<Register>>) -> impl Responder {
    let Register { username, country } = form.into_inner();
    format!("Hello {username} from {country}!")
}

#[actix_web::main]
async fn main() -> Result<()> {
    HttpServer::new(|| App::new().service(ping).service(register))
        .bind(("127.0.0.1", 8090))
        .unwrap()
        .run()
        .await
}
