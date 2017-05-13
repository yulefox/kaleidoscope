#!/bin/sh

gitbook-gen --exclusions _book,notes --show-all . \
    > SUMMARY.md