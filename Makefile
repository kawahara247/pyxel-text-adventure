.PHONY: push

# kawahara247アカウントでGitHubにプッシュ
push:
	GITHUB_TOKEN= gh auth switch --user kawahara247
	GITHUB_TOKEN= git push --set-upstream origin HEAD
