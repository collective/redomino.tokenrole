#!/bin/sh

PRODUCTNAME='redomino.tokenrole'

i18ndude rebuild-pot --pot locales/${PRODUCTNAME}.pot --create ${PRODUCTNAME} .

i18ndude sync --pot locales/${PRODUCTNAME}.pot locales/*/LC_MESSAGES/${PRODUCTNAME}.po

# Compile po files
for lang in $(find locales -mindepth 1 -maxdepth 1 -type d); do
    if test -d $lang/LC_MESSAGES; then
        msgfmt -o $lang/LC_MESSAGES/${PRODUCTNAME}.mo $lang/LC_MESSAGES/${PRODUCTNAME}.po
    fi
done

OTHER_DOMAINS="plone"
# Compile po files
for other_domain in $OTHER_DOMAINS; do
    i18ndude sync --pot locales/${other_domain}.pot locales/*/LC_MESSAGES/${other_domain}.po
    for lang in $(find locales -mindepth 1 -maxdepth 1 -type d); do
        if test -d $lang/LC_MESSAGES; then
            msgfmt -o $lang/LC_MESSAGES/${other_domain}.mo $lang/LC_MESSAGES/${other_domain}.po
        fi
    done
done


