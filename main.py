# AWS IoT Sample Runner
# Cole Brooks
# Automatically runs all AWS IoT samples using certificates and keys

import requests
import os
import platform

current_dir = os.getcwd()
python_command = "python3" if platform.system() == "Linux" else "py"


def run_pubsub(args):
    endpoint = args["endpoint"]
    root_ca_path = args["ca_file"]
    certificate_path = args["cert"]
    private_key_path = args["key"]

    os.system(f"{python_command} samples/pubsub.py --endpoint {endpoint} --ca_file {root_ca_path} --cert {certificate_path} --key {private_key_path}")


def run_shadow(args):
    endpoint = args["endpoint"]
    root_ca_path = args["ca_file"]
    certificate_path = args["cert"]
    private_key_path = args["key"]
    thing_name = args["thing_name"]

    os.system(f"{python_command} samples/shadow.py --endpoint {endpoint} --ca_file {root_ca_path} --cert {certificate_path} --key {private_key_path} --thing_name {thing_name}")


def find_file(file_type, file_dir):
    for file in os.listdir(file_dir):
        if file.endswith(file_type):
            # return the file and the path to the file
            return file, os.path.abspath(f"{file_dir}/{file}")


def install_sample(sample_name):
    sample_content = download_sample(sample_name)
    write_sample_file(sample_name, sample_content)


def write_sample_file(sample_name, sample_content):
    if not os.path.exists(f"{current_dir}/samples"):
        os.mkdir(f"{current_dir}/samples")
    file_name = f"{current_dir}/samples/{sample_name}.py"
    with open(file_name, "w") as sample:
        sample.write(sample_content)


def download_sample(sample):
    return requests.get(f"https://raw.githubusercontent.com/aws/aws-iot-device-sdk-python-v2/main/samples/{sample}.py").text


def main():
    # install command line utils
    install_sample("command_line_utils")

    # ask the user for the samples they want to run
    samples = input("Enter the samples you want to run (separated by spaces): ").split(" ")

    # read the certs and keys from a specified directory
    certs_dir = input("Enter the directory containing your certificates and keys: ")

    root_ca, root_ca_path = find_file(".pem", certs_dir)
    private_key, private_key_path = find_file("private.pem.key", certs_dir)
    certificate, certificate_path = find_file(".pem.crt", certs_dir)

    endpoint = input("Enter your AWS IoT endpoint: ")

    # run the sample using the certs and keys
    for sample in samples:
        install_sample(sample)
        if sample == "pubsub":
            args = {
                "endpoint": endpoint,
                "ca_file": root_ca_path,
                "cert": certificate_path,
                "key": private_key_path
            }

            run_pubsub(args)

        elif sample == "shadow":
            args = {
                "endpoint": endpoint,
                "ca_file": root_ca_path,
                "cert": certificate_path,
                "key": private_key_path,
                "thing_name": input("Enter your thing name: ")
            }

            run_shadow(args)
        try:
            os.system(f"{python_command} samples/{sample}.py --endpoint {endpoint} --ca_file {root_ca_path} --cert {certificate_path} --key {private_key_path}")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
