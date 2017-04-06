// Copyright (c) 2017 Yule Fox
// All rights reserved

#include "http.h"

static struct mg_mgr mgr;
static const char *s_http_port = "8000";
static struct mg_serve_http_opts s_http_server_opts;

static void handle_cmd(struct mg_connection *nc, struct http_message *hm)
{
  const struct mg_str *cmd = NULL;

  if (mg_vcasecmp(&hm->method, "GET") == 0) {
    cmd = &hm->query_string;
  } else if (mg_vcasecmp(&hm->method, "POST") == 0) {
    cmd = &hm->body;
  }

  mg_printf(nc, "%s", "HTTP/1.1 200 OK\nTransfer-Encoding: chunked\n\n");
  mg_printf_http_chunk(nc, "{ \"cmd\": \"%.*s\" }", cmd->len, cmd->p);
  printf("%.*s\n", (int)(cmd->len), cmd->p);
  mg_send_http_chunk(nc, "", 0);
}

static void ev_handler(struct mg_connection *nc, int ev, void *p)
{
  struct http_message *hm = (struct http_message *) p;

  if (ev == MG_EV_HTTP_REQUEST) {
    if (mg_vcmp(&hm->uri, "/api/v1/cmd") == 0) {
      handle_cmd(nc, hm);
    } else {
      mg_serve_http(nc, hm, s_http_server_opts);
    }
  }
}

int http_init(void)
{
  struct mg_connection *nc;

  mg_mgr_init(&mgr, NULL);
  printf("Starting web server on port %s\n", s_http_port);
  nc = mg_bind(&mgr, s_http_port, ev_handler);
  if (nc == NULL) {
    printf("Failed to create listener\n");
    return 1;
  }

  // Set up HTTP server parameters
  mg_set_protocol_http_websocket(nc);
  s_http_server_opts.document_root = ".";  // Serve current directory
  s_http_server_opts.enable_directory_listing = "yes";
  return 0;
}

int http_loop(void)
{
    mg_mgr_poll(&mgr, 0);
    return 0;
}

int http_fini(void)
{
    mg_mgr_free(&mgr);
    return 0;
}
