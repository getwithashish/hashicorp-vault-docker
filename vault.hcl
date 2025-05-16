storage "s3" {
  bucket             = "secret-store"
  region             = "ap1"
  endpoint           = "https://gateway.storjshare.io"
  s3_force_path_style = true
}

listener "tcp" {
  address       = "0.0.0.0:8200"
  tls_disable   = true
}

disable_mlock = true
api_addr = "http://localhost:8200"
ui = true
