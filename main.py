from github import Github
from dotenv import load_dotenv
import base64
import os

load_dotenv()

g = Github(os.environ.get("G_TOKEN"))

user = g.get_user()
profile_repo = user.get_repo("newtyf")
last_updated_repo_name = user.get_repos(sort="pushed")[0].name
last_updated_repo_link = user.get_repos(sort="pushed").__getitem__(0).html_url

def update_readme(match_line: str, replace: str, content: str) -> str:
  split_lines_readme = content.split('\n')

  for index, line in enumerate(split_lines_readme):
    if match_line in line:
        split_lines_readme[index] = replace

  modify_content = "\n".join(split_lines_readme)
  return modify_content

def commitReadme(message: str, path: str, sha: str, content: str):
  profile_repo.update_file(path=path, message=message, sha=sha, content=content)

file_readme = profile_repo.get_contents('README.md')
readme_content = file_readme.decoded_content.decode()

replace_content = f"- \U0001f52d I\u2019m currently working on [{last_updated_repo_name.upper()}]({last_updated_repo_link})."

readme_content = update_readme(match_line="currently working",replace=replace_content, content=readme_content)

commitReadme(message="Update README", path=file_readme.path, sha=file_readme.sha, content=readme_content)
