import json
import os

from main import main  # main.pyをインポート

# プロジェクトのルートディレクトリを取得
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# config.yaml のパスを確認
config_path = os.path.join(BASE_DIR, "config/config.yaml")
if not os.path.exists(config_path):
    # config.yaml を生成
    with open(config_path, "w") as f:
        f.write("""\
template_dir: "templates"
output_dir: "terraform"
default_repository:
  visibility: "public"
default_team:
  privacy: "closed"
  role: "member"
default_membership:
  role: "member"
""")

# Terraform の状態ファイルパスを確認
terraform_dir = os.path.join(BASE_DIR, "terraform")
os.makedirs(terraform_dir, exist_ok=True)
tfstate_path = os.path.join(terraform_dir, "terraform.tfstate")
if not os.path.exists(tfstate_path):
    # terraform.tfstate を生成
    with open(tfstate_path, "w") as f:
        f.write(json.dumps({
            "version": 4,
            "terraform_version": "1.4.5",
            "resources": []
        }))

# 環境変数を設定
os.environ["REPOSITORIES"] = json.dumps([
    {
        "repository_name": "repo1",
        "description": "This is repo1",
        "visibility": "public",
        "gitignore_template": "Python"
    }
])

os.environ["TEAMS"] = json.dumps([
    {
        "team_name": "team1",
        "description": "Updated team",
        "privacy": "closed",
        "members": [{"username": "user1", "role": "maintainer"}]
    }
])

# MEMBERSHIPS を追加（全員 "member" とする）
os.environ["MEMBERSHIPS"] = json.dumps([
    "user1",
    "user2",
    "user3"
])

# 作業ディレクトリをプロジェクトルートに変更
os.chdir(BASE_DIR)

# main.pyを呼び出して実行
if __name__ == "__main__":
    # 必要ならカスタムの出力ディレクトリを指定可能
    custom_output_dir = os.path.join(BASE_DIR, "terraform")
    main(output_dir_override=custom_output_dir)
