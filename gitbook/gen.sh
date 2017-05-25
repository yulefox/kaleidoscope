#!/bin/sh

usage()
{
    echo USAGE: $0 [-abc]
    echo "  -a Generate all"
    echo "  -b Generate private essays"
    echo "  -c Generate technology notes"
}

if [[ $# -eq 0 ]] ; then
    usage
    exit 1
fi

rm -rf _book

while getopts "abc" opt ; do
    case $opt in
        a)
            gitbook-gen --exclusions _book,node_modules --show-all . \
                > SUMMARY.md
            echo "Generate all, OK"
            ;;
        b)
            gitbook-gen --exclusions _book,node_modules,notes --show-all . \
                > SUMMARY.md
            echo "Generate essays, OK"
            ;;
        c)
            gitbook-gen --exclusions _book,node_modules,arts,essays --show-all . \
                > SUMMARY.md
            echo "Generate notes, OK"
            ;;
        ?)
            usage
            exit 0
            ;;
    esac
done
shift $(($OPTIND - 1))
