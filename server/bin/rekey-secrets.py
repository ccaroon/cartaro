#!/usr/bin/env python
################################################################################
import argparse
import os
import pprint
import sys

sys.path.append(".")
from cartaro.model.secret import Secret
################################################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Re-key Encrypted Secret Data')
    parser.add_argument('old_key', type=str, help='Old Key')
    parser.add_argument('new_key', type=str, help='New Key')
    args = parser.parse_args()

    env = os.getenv('CARTARO_ENV')
    if not env:
        raise Exception("CARTARO_ENV **must** be set.")

    doc_path = os.getenv('CARTARO_DOC_PATH')
    if not doc_path:
        raise Exception("CARTARO_DOC_PATH **must** be set.")

    print(F"Re-keying Secrets for '{env}' in '{doc_path}'")

    Secret.ENCRYPTION_KEY = args.old_key
    secrets = Secret.fetch()

    for secret in secrets:
        is_deleted = secret.deleted_at
        if is_deleted:
            # Undelete b/c can't save a deleted object
            print(f"Undeleting '{secret.name}'")
            secret.undelete()
            # Re-load to ensure object in memory matches record in db.
            secret.load()

        print(f"Rekeying '{secret.name}'")
        secret.rekey(args.new_key)

        if is_deleted:
            print(f"Re-Deleting '{secret.name}'")
            secret.delete(safe=True)

    print(F"*** Remember to update your CartaroCfg.json file! ***")
