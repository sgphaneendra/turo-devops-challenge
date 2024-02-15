#!/usr/bin/env python3.11
import json
import hcl2
import sys
from git import Repo
import git
import os
import subprocess
import requests



class TagUpdate:
    def __init__(self, new_image_tag):
        self.new_image_tag = new_image_tag
        self.github_repository = 'turo-devops-challenge'
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.branch_name = f'release-{new_image_tag}'
        self.uri = "https://api.github.com"
        self.header = {
            'Authorization': f'Bearer {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'}
        self.user_login = 'sgphaneendra'

    def get_user_info(self):
        print(f"Getting user info for {self.user_login}...")

        response = requests.get(
            f"{self.uri}/users/{self.user_login}",
            headers=self.header
        )
        data = response.json()
        user = data.get("name", self.user_login)
        user_email = data.get("email", f"{self.user_login}@users.noreply.github.com")
        if user_email is None:
            user_email = f"{self.user_login}@users.noreply.github.com"
        return user, user_email

    def git_config(self):
        print("Configuring git...")
        self.user, self.user_email = self.get_user_info()
        subprocess.run(["git", "config", "--global", "--add", "safe.directory", "/github/workspace"])
        subprocess.run(["git", "config", "--global", "user.email", str(self.user_email)])
        subprocess.run(["git", "config", "--global", "user.name", str(self.user)])

    def update_image_tag(self):
        try:
            with open("terraform/terraform.tfvars", "r") as file_in:
                data = hcl2.load(file_in)

            data["image_name"] = "sgphaneendra/nginx-static-app:" + self.new_image_tag

            with open("terraform/terraform.tfvars", "w") as file_out:
                file_out.write(json.dumps(data, indent=4))

        except Exception as e:
            print(f"Error updating image tag: {e}")

    def create_or_checkout_branch(self):
        try:
            # Check if branch exists
            subprocess.run(['git', 'rev-parse', '--verify', "--quiet", self.branch_name], check=True, stdout=subprocess.PIPE)
            print(f"Branch {self.branch_name} already exists. Skipping branch creation.")
            subprocess.run(['git', 'checkout', self.branch_name])
            subprocess.run(['git', 'pull', 'origin', self.branch_name])
            subprocess.run(['git', 'pull', 'origin', 'main'])
        except subprocess.CalledProcessError:
            # Create a new branch
            print(f"Creating the new branch: {self.branch_name}")
            subprocess.run(['git', 'checkout', '-b', self.branch_name])
            subprocess.run(['git', 'pull', 'origin', 'main'])
            print(f"Created and checked out branch: {self.branch_name}")

    def commit_and_push_changes(self):
        try:
            # Check if there are changes to commit
            status_output = subprocess.run(['git', 'status', '--porcelain'], stdout=subprocess.PIPE, universal_newlines=True)
            if not status_output.stdout.strip():
                print("No changes to commit. Skipping commit and push.")
                return

            # Commit changes
            subprocess.run(['git', 'add', 'terraform/terraform.tfvars'])
            subprocess.run(['git', 'commit', '-m', f'Update image tag to {self.new_image_tag}'])
            subprocess.run(['git', 'push', '-u', 'origin', self.branch_name])

            print("Changes committed and pushed to the repository")

        except Exception as e:
            print(f"Error committing and pushing changes: {e}")

    def check_pull_request_exists(self):
        try:
            response = requests.get(
                f"{self.uri}/repos/{self.github_repository}/pulls",
                headers=self.header
            )
            pull_requests = response.json()
            for pr in pull_requests:
                if pr['head']['ref'] == self.branch_name:
                    print("Pull request already exists. Skipping creation.")
                    return True
            return False
        except Exception as e:
            print(f"Error checking pull request: {e}")
            return False

    def create_pull_request(self, pr_title, pr_body):
        try:
            self.git_config()
            self.create_or_checkout_branch()
            self.update_image_tag()
            self.commit_and_push_changes()
            if self.check_pull_request_exists():
                return
            else:
                subprocess.run(['gh', 'pr', 'create', '--base', 'main', '--head', self.branch_name, '--title', pr_title, '--body', pr_body])
                print(f"Pull request created for branch: {self.branch_name}")
        except Exception as e:
            print(f"Error creating pull request: {e}")


if __name__ == '__main__':
    new_image_tag = sys.argv[1]
    pr_title = f'Update latest WebApp image tag to {new_image_tag}'
    pr_body = 'Updating the image tag in the terraform.tfvars file.'

    updater = TagUpdate(new_image_tag)
    updater.create_pull_request(pr_title, pr_body)
