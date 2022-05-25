use std::fs;
use std::{error, process};

use clap::Parser;

#[derive(Parser, Debug)]
pub struct Arguments {
    /// search hint
    #[clap(short, long)]
    search: String,

    /// file hint
    #[clap(short, long)]
    file: String,
}

pub fn run(args: &Arguments) -> Result<(), Box<dyn error::Error>> {
    let contents = fs::read_to_string(&args.file)?;

    println!("content:\n{}", contents);
    Ok(())
}

fn main() {
    let args = Arguments::parse();
    println!("searching for {:?} in {}", args.search, args.file);
    if let Err(e) = run(&args) {
        eprintln!("error: {}", e);
        process::exit(1)
    }
    println!("{:?}", args);
}
